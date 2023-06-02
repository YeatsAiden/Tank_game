<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="ordinary_tileset" tilewidth="8" tileheight="8" tilecount="128" columns="16">
 <image source="tile_set.png" width="128" height="64"/>
 <tile id="3" probability="0.01"/>
 <tile id="4" probability="0.01"/>
 <tile id="5" probability="0.01"/>
 <wangsets>
  <wangset name="plants" type="mixed" tile="-1">
   <wangcolor name="weeds" color="#ff0000" tile="-1" probability="0.01"/>
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
  <wangset name="rock" type="mixed" tile="-1">
   <wangcolor name="top" color="#ff0000" tile="-1" probability="1"/>
   <wangcolor name="back" color="#00ff00" tile="-1" probability="1"/>
   <wangcolor name="rigth" color="#0000ff" tile="-1" probability="1"/>
   <wangcolor name="front" color="#ff7700" tile="-1" probability="1"/>
   <wangcolor name="left" color="#00e9ff" tile="-1" probability="1"/>
   <wangtile tileid="53" wangid="0,2,0,5,5,5,5,0"/>
   <wangtile tileid="54" wangid="2,2,2,0,5,5,0,2"/>
   <wangtile tileid="57" wangid="2,2,2,2,2,2,2,2"/>
   <wangtile tileid="60" wangid="2,2,0,3,0,0,2,2"/>
   <wangtile tileid="61" wangid="0,0,3,3,3,3,0,2"/>
   <wangtile tileid="69" wangid="5,5,5,5,5,5,5,5"/>
   <wangtile tileid="70" wangid="5,5,5,5,5,5,5,5"/>
   <wangtile tileid="71" wangid="2,2,1,1,1,5,5,0"/>
   <wangtile tileid="72" wangid="2,2,1,1,1,1,1,2"/>
   <wangtile tileid="73" wangid="2,2,1,1,1,1,1,2"/>
   <wangtile tileid="74" wangid="2,2,1,1,1,1,1,2"/>
   <wangtile tileid="75" wangid="2,0,3,3,1,1,1,2"/>
   <wangtile tileid="76" wangid="3,3,3,3,3,3,3,3"/>
   <wangtile tileid="77" wangid="3,3,3,3,3,3,3,3"/>
   <wangtile tileid="87" wangid="1,1,1,0,0,0,5,5"/>
   <wangtile tileid="88" wangid="1,1,1,0,0,0,1,1"/>
   <wangtile tileid="89" wangid="1,1,1,0,0,0,1,1"/>
   <wangtile tileid="90" wangid="1,1,1,0,0,0,1,1"/>
   <wangtile tileid="91" wangid="1,3,3,0,0,0,1,1"/>
   <wangtile tileid="101" wangid="5,5,5,5,5,5,5,5"/>
   <wangtile tileid="102" wangid="5,0,4,4,4,0,0,5"/>
   <wangtile tileid="105" wangid="4,4,4,4,4,4,4,4"/>
   <wangtile tileid="108" wangid="3,3,0,0,4,4,4,0"/>
   <wangtile tileid="109" wangid="3,3,3,3,3,3,3,3"/>
   <wangtile tileid="117" wangid="5,0,4,4,4,0,5,5"/>
   <wangtile tileid="118" wangid="4,4,4,4,4,4,4,4"/>
   <wangtile tileid="121" wangid="4,4,4,4,4,4,4,4"/>
   <wangtile tileid="124" wangid="4,4,4,4,4,4,4,4"/>
   <wangtile tileid="125" wangid="3,3,3,0,4,4,4,0"/>
  </wangset>
 </wangsets>
</tileset>
