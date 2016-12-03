d3.csv("/Users/Frank/Documents/UCSC/TIM_209/project/demo/test/population.csv", function(data) {
var dataobj = { children: data };
var pack = d3.layout.pack();
pack = pack.padding(2).size([800,600]);
var nodes = pack.nodes(dataobj);
nodes = nodes.filter(function(it) { return it.parent; });
var color = d3.scale.category20();
d3.select("svg")
  .selectAll("circle")                 // 建立 circle 的 Selection
  .data(nodes)                         // 綁定 selection 與資料
  .enter()                             // 對於任何沒被對應而落單的資料 ...
  .append("circle")                    // 新增一個 circle 標籤
  .attr({
    cx: function(it) { return it.x; }, // 用 x,y 當圓心
    cy: function(it) { return it.y; },
    r : function(it) { return it.r; }, // 用 r 當半徑
    fill: function(it) { return color(it.country); },
    stroke: "#444",                    // 邊框畫深灰色
  });


d3.select("svg").selectAll("text").data(nodes).enter()
  .append("text")
  .attr("x", function(it){ return it.x; })
  .attr("y", function(it){ return it.y + 5; })
  .attr("text-anchor", "middle")
  .text(function(it)  { return it["country"]; }); // 設定文字為國名

});