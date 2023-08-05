//
// Created by nbdy on 31.12.21.
//

#ifndef MAPRENDERCACHE_H_
#define MAPRENDERCACHE_H_

#include <filesystem>
#include <mapbox2mapnik/mapbox2mapnik.hpp>
#include <mapnik/agg_renderer.hpp>
#include <mapnik/datasource_cache.hpp>
#include <mapnik/image_util.hpp>
#include <mapnik/load_map.hpp>
#include <mapnik/map.hpp>
#include <mapnik/projection.hpp>
#include <mapnik/version.hpp>
#include <sstream>
#include <string>

// https://github.com/mapnik/mapnik/wiki/PostGIS
// https://github.com/mapnik/mapnik/wiki/OptimizeRenderingWithPostGIS

static const char* const LONGLAT = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";
static const char* const MERC = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over";

class MapRenderCache {
  mapnik::projection m_Proj_longlat = mapnik::projection(LONGLAT);
  mapnik::projection m_Proj_merc = mapnik::projection(MERC);
  mapnik::proj_transform m_Transform;

  std::filesystem::path m_sMapnikXMLPath;

  mapnik::Map m_Map;

  uint32_t m_u32RenderedImageWidth;
  uint32_t m_u32RenderedImageHeight;

  std::filesystem::path m_CacheDirectory;

 protected:
  void createCacheDirectory() {
    if(!std::filesystem::exists(m_CacheDirectory)) {
      std::filesystem::create_directories(m_CacheDirectory);
    }
  }

  std::filesystem::path getTileFilename(double i_dX, double i_dY, int32_t i_i32Z, uint32_t i_u32Width, uint32_t i_u32Height) {
    std::stringstream r;
    auto x = floor(i_dX * 1000) / 1000;
    auto y = floor(i_dY * 1000) / 1000;
    r << "x" << std::to_string(x);
    r << "y" << std::to_string(y);
    r << "z" << std::to_string(i_i32Z);
    r << "w" << std::to_string(i_u32Width);
    r << "h" << std::to_string(i_u32Height);
    r << ".png";
    return m_CacheDirectory / r.str();
  }

  mapnik::box2d<double> getBoundingBox(double i_dX, double i_dY, uint32_t i_i32Z) const {
    auto dx = ((20037508.34 * 2 * (static_cast<double>(m_u32RenderedImageWidth) / 2))) / (256 * (pow(2.0, i_i32Z)));
    auto minx = i_dX - dx;
    auto maxx = i_dX + dx;
    return {minx, i_dX - 10, maxx, i_dY + 10};
  }

  void renderImage(double i_dX, double i_dY, uint32_t i_i32Z, const std::string& i_sFilePath) {
    mapnik::image_rgba8 m_RenderedImage(static_cast<int>(m_u32RenderedImageWidth), static_cast<int>(m_u32RenderedImageHeight));
    mapnik::agg_renderer<mapnik::image_rgba8> m_Renderer(m_Map, m_RenderedImage);
    m_Map.set_aspect_fix_mode(mapnik::Map::aspect_fix_mode::ADJUST_BBOX_HEIGHT);
    double _z = i_i32Z;
    m_Transform.forward(i_dX, i_dY, _z);
    m_Map.zoom_to_box(getBoundingBox(i_dX, i_dY, i_i32Z));
    m_Renderer.apply();
    mapnik::save_to_file(m_RenderedImage, i_sFilePath, "png8");
  }

  static std::filesystem::path getMapnikInputPath(const std::string& i_sType) {
    std::stringstream v;
    v << std::to_string(MAPNIK_MAJOR_VERSION) << "." << std::to_string(MAPNIK_MINOR_VERSION);
    std::filesystem::path r("/usr/lib/mapnik");
    r = r / v.str() / "input" / (i_sType + ".input");
    return r;
  }

  void setup() {
    createCacheDirectory();
    mapnik::datasource_cache::instance().register_datasource(getMapnikInputPath("postgis"));
    mapnik::datasource_cache::instance().register_datasource(getMapnikInputPath("shape"));
    m_Map.set_aspect_fix_mode(mapnik::Map::aspect_fix_mode::aspect_fix_mode_MAX);
    m_Map.set_srs(MERC);
    mapnik::load_map(m_Map, m_sMapnikXMLPath);
  }

 public:
  explicit MapRenderCache(const char* i_sMapnikXML,
                          int32_t i_i32Width = 256,
                          int32_t i_i32Height = 256) : m_Transform(m_Proj_longlat, m_Proj_merc),
                                                       m_sMapnikXMLPath(i_sMapnikXML),
                                                       m_Map(i_i32Width, i_i32Height),
                                                       m_u32RenderedImageWidth(i_i32Width),
                                                       m_u32RenderedImageHeight(i_i32Height),
                                                       // m_RenderedImage(i_i32Width, i_i32Height),
                                                       // m_Renderer(m_Map, m_RenderedImage),
                                                       m_CacheDirectory("cache")
  {
    setup();
  };

  explicit MapRenderCache(const char* i_sMapnikXML,
                          const char* i_sCacheDirectory,
                          int32_t i_i32Width = 256,
                          int32_t i_i32Height = 256) : m_Transform(m_Proj_longlat, m_Proj_merc),
                                                       m_sMapnikXMLPath(i_sMapnikXML),
                                                       m_Map(i_i32Width, i_i32Height),
                                                       m_u32RenderedImageWidth(i_i32Width),
                                                       m_u32RenderedImageHeight(i_i32Height),
                                                       // m_RenderedImage(i_i32Width, i_i32Height),
                                                       // m_Renderer(m_Map, m_RenderedImage),
                                                       m_CacheDirectory(i_sCacheDirectory)
  {
    setup();
  };

  std::string getTile(double i_dX, double i_dY, int32_t i_i32Z) {
    auto fp = absolute(getTileFilename(i_dX, i_dY, i_i32Z, m_u32RenderedImageWidth, m_u32RenderedImageHeight));
    if (!std::filesystem::exists(fp)) {
      renderImage(i_dX, i_dY, i_i32Z, fp);
    }
    return fp;
  }
};

#endif//MAPRENDERCACHE_H_
