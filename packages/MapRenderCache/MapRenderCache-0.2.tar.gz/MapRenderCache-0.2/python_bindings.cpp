//
// Created by nbdy on 31.12.21.
//

#include <pybind11/pybind11.h>

#include "MapRenderCache.h"


PYBIND11_MODULE(MapRenderCache, m) {
  pybind11::class_<MapRenderCache> cls(m, "MapRenderCache");

  // Constructor
  cls.def(pybind11::init([](const char* i_sMapnikXMLPath) {
    return new MapRenderCache(i_sMapnikXMLPath);
  }));
  cls.def(pybind11::init([](const char* i_sMapnikXMLPath, int i_u32Width, int i_u32Height){
    return new MapRenderCache(i_sMapnikXMLPath, i_u32Width, i_u32Height);
  }));
  cls.def(pybind11::init([](const char* i_sMapnikXMLPath, const char* i_sCacheDirectory, int i_u32Width, int i_u32Height){
    return new MapRenderCache(i_sMapnikXMLPath, i_sCacheDirectory, i_u32Width, i_u32Height);
  }));

  // Member functions
  cls.def("get_tile",
          static_cast<std::string (MapRenderCache::*)(double, double, int32_t)>(&MapRenderCache::getTile));
  cls.def("get_tile",
          static_cast<std::string (MapRenderCache::*)(int32_t, int32_t, int32_t)>(&MapRenderCache::getTile));

  // Static functions
  m.def("longitude2x", &MapRenderCache::longitude2x);
  m.def("latitude2y", &MapRenderCache::latitude2y);
  m.def("x2longitude", &MapRenderCache::x2longitude);
  m.def("y2latitude", &MapRenderCache::y2latitude);
}
