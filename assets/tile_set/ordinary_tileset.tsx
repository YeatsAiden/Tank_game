<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="ordinary_tileset" tilewidth="8" tileheight="8" tilecount="512" columns="32">
 <image source="tile_set.png" width="256" height="128"/>
 <tile id="3" probability="0.01"/>
 <tile id="4" probability="0.01"/>
 <tile id="5" probability="0.01"/>
 <wangsets>
  <wangset name="plants" type="mixed" tile="-1">
   <wangcolor name="weeds" color="#ff0000" tile="-1" probability="0.01"/>
   <wangtile tileid="3" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="4" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="5" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="35" wangid="1,1,1,1,1,1,1,1"/>
  </wangset>
  <wangset name="rock" type="mixed" tile="-1">
   <wangcolor name="top" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="38" wangid="0,1,1,1,1,1,0,0"/>
   <wangtile tileid="39" wangid="0,0,0,1,1,1,1,1"/>
   <wangtile tileid="70" wangid="1,1,1,1,0,0,0,1"/>
   <wangtile tileid="71" wangid="1,1,0,0,0,1,1,1"/>
   <wangtile tileid="73" wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="74" wangid="0,0,0,1,1,1,0,0"/>
   <wangtile tileid="75" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="105" wangid="0,1,1,1,0,0,0,0"/>
   <wangtile tileid="106" wangid="1,1,1,1,1,1,1,1"/>
   <wangtile tileid="107" wangid="0,0,0,0,0,1,1,1"/>
   <wangtile tileid="137" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="138" wangid="1,1,0,0,0,0,0,1"/>
   <wangtile tileid="139" wangid="0,0,0,0,0,0,0,1"/>
  </wangset>
 </wangsets>
</tileset>
