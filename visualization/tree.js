const treeData = [];
const flatNodes = [];

fetch("/dist/categories-coded.json")
.then(data => data.json())
.then(jsonData => {
  const maxLevel = Math.max(...jsonData.categories.map(category => category.level));
  for(let i = 0; i <= maxLevel; i++) {
    jsonData.categories.forEach(category => {
      if (category.level !== i) {
        return;
      }

      const node = {
        parent: null,
        _children: [],
        children: [],
        ...category
      };
      flatNodes.push(node);

      if (category.level === 0) {
        treeData.push(node);
        return;
      }
      const parentCode = node.code.substring(0, node.code.length-4);

      let parentNode = flatNodes.find(node => {
        return node.code === parentCode;
      });
      if (!parentNode) console.log(node);
      parentNode._children.push(node);
      node.parent = parentNode;
    });
  }

  flatNodes.forEach(node => {
    if (!node._children.length) {
      node.children = null;
      node._children = null;
    }
  });
}).then(() => {

  var margin = {top: 20, right: 120, bottom: 20, left: 200},
  	width = innerWidth - margin.right - margin.left,
  	height = innerHeight - margin.top - margin.bottom;
  	
  var i = 0,
  	duration = 750,
  	root;

  var tree = d3.layout.tree()
  	.size([height, width]);

  var diagonal = d3.svg.diagonal()
  	.projection(function(d) { return [d.y, d.x]; });

  var svg = d3.select("body").append("svg")
  	.attr("width", width + margin.right + margin.left)
  	.attr("height", height + margin.top + margin.bottom)
    .append("g")
  	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  root = treeData[0];
  root.x0 = height / 2;
  root.y0 = 0;
    
  update(root);

  d3.select(self.frameElement).style("height", "500px");

  function update(source) {
    const infoBox = document.querySelector("#category-information");
    infoBox.querySelector("#name").innerHTML = source.name;
    infoBox.querySelector("#description").innerHTML = source.description;
    infoBox.querySelector("#code").innerHTML = source.code;

    var circleRadius = 10;
    var paddingLeftRight = 18; // adjust the padding values depending on font and font size
    var paddingTopBottom = 5;

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
      links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 180; });

    // Update the nodes…
    var node = svg.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .on("click", click);

    nodeEnter.append("circle")
      .attr("r", 1e-6)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

    let nodeGradient = nodeEnter.append("linearGradient")
      .attr("id", "boxGradient")
      .attr("x1", "0%")
      .attr("x2", "0%")
      .attr("y1", "0%")
      .attr("y2", "100%");

    nodeGradient.append("stop")
      .attr("offset", "0%")
      .attr("stop-color", "white")
      .attr("stop-opacity", 0.4);

    nodeGradient.append("stop")
      .attr("offset", "50%")
      .attr("stop-color", "white")
      .attr("stop-opacity", 1);

    nodeGradient.append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "white")
      .attr("stop-opacity", 0.4);

      nodeEnter.append("rect")
      .style("opacity", 1e-6)
      .attr("fill", "url(#boxGradient)");

    nodeEnter.append("text")
      .attr("x", function(d) { return d.children || d._children ? -circleRadius*2 : circleRadius*2; })
      .attr("dy", "5.6px")
      .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1e-6);

    nodeEnter.selectAll("text").each(function(d) {
        d.bb = this.getBBox(); // get bounding box of text field and store it in texts array
    });
    nodeEnter.selectAll("rect")
      .attr('class', 'node-box')
      .attr("x", function (d) {
        const F = (d.children || d._children ? -1 : 0);
        return F * d.bb.width + F * paddingLeftRight + (2*F+1) * (circleRadius + 3);
      })
      .attr("y", function(d) { return -d.bb.height + paddingTopBottom; })
      .attr("width", function(d) { return d.bb.width + paddingLeftRight; })
      .attr("height", function(d) { return d.bb.height + paddingTopBottom; });

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
  	  .duration(duration)
  	  .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    nodeUpdate.select("circle")
  	  .attr("r", circleRadius)
  	  .style("fill", function(d) {
        if (d._children) return "lightsteelblue";
        if (d.code === source.code) return "#9ACD32";
        return "#fff";
      });

    nodeUpdate.select("text")
      .style("fill-opacity", 1);
    nodeUpdate.select("rect")
  	  .style("opacity", 1); //function (d) { return d.children || d._children ? 1 : 1e-6 });

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
  	  .duration(duration)
  	  .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
  	  .remove();

    nodeExit.select("circle")
  	  .attr("r", 1e-6);

    nodeExit.select("text")
      .style("fill-opacity", 1e-6);
    nodeExit.select("rect")
  	  .style("opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
  	  .data(links, function(d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
  	  .attr("class", "link")
  	  .attr("d", function(d) {
    		var o = {x: source.x0, y: source.y0};
    		return diagonal({source: o, target: o});
  	  });

    // Transition links to their new position.
    link.transition()
  	  .duration(duration)
  	  .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
  	  .duration(duration)
  	  .attr("d", function(d) {
    		var o = {x: source.x, y: source.y};
    		return diagonal({source: o, target: o});
  	  })
  	  .remove();

    // Stash the old positions for transition.
    nodes.forEach(function(d) {
    	d.x0 = d.x;
    	d.y0 = d.y;
    });
  }

  function closeNode(node) {
    if (!node.children) {
      return;
    }
    node._children = node.children;
    node.children = null;
    update(node);
  }

  function openNode(node) {
    if (node.children) {
      return;
    }
    node.children = node._children;
    node._children = null;
    update(node);
  }
  function toggleNode(node) {
    if (node.children) {
      closeNode(node);
    } else {
      openNode(node);
    }
  }

  // Toggle children on click.
  function click(d) {
    if (d.parent) {
      d.parent.children.forEach(child => {
        if (child !== d) {
          closeNode(child);
        }
      });
    }

    toggleNode(d);
  }
});
