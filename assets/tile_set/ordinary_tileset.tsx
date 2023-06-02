<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="ordinary_tileset" tilewidth="8" tileheight="8" tilecount="128" columns="16">
 <image source="tile_set.png" width="128" height="64"/>
 <wangsets>
  <wangset name="dirt" type="mixed" tile="-1">
   <wangcolor name="dirt" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="3" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="4" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="5" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="19" wangid="1,1,1,1,1,1,1,1"/>
  </wangset>
  <wangset name="walls" type="mixed" tile="-1">
   <wangcolor name="brownwalls" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="0" wangid="0,0,1,0,1,0,0,0"/>
   <wangtile tileid="1" wangid="0,0,1,0,0,0,1,0"/>
   <wangtile tileid="2" wangid="0,0,0,0,1,0,1,0"/>
   <wangtile tileid="16" wangid="1,0,0,0,1,0,0,0"/>
   <wangtile tileid="18" wangid="1,0,0,0,1,0,0,0"/>
   <wangtile tileid="32" wangid="1,0,1,0,0,0,0,0"/>
   <wangtile tileid="33" wangid="0,0,1,0,0,0,1,0"/>
   <wangtile tileid="34" wangid="1,0,0,0,0,0,1,0"/>
  </wangset>
 </wangsets>
</tileset>
