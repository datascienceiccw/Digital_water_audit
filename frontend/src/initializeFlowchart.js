export const initializeFlowchart = (sourceWaterFlowData) => {
  const nodesMap = new Map();
  const levelsMap = new Map();
  const edges = [];
  const adjacencyList = new Map();

  sourceWaterFlowData.forEach(item => {
    const source = item.fields.source;
    const destination = item.fields.destination;
    const volume = parseFloat(item.fields.volume); 

    if (!nodesMap.has(source)) {
      nodesMap.set(source, {
        id: `node-${source.replace(/\s+/g, '-')}`,
        type: 'sourceNode', // Consider dynamic type assignment if needed in future
        data: { label: source }
      });
    }
    if (!nodesMap.has(destination)) {
      nodesMap.set(destination, {
        id: `node-${destination.replace(/\s+/g, '-')}`,
        type: 'treatmentNode', // Consider dynamic type assignment if needed in future
        data: { label: destination }
      });
    }

    const edgeId = `e-${nodesMap.get(source).id}-${nodesMap.get(destination).id}`;
    edges.push({
      id: edgeId,
      source: nodesMap.get(source).id,
      target: nodesMap.get(destination).id,
      type: 'waterEdge',
      data: { consumption: volume.toFixed(2) }, // Check volume is a number
      animated: true,
    });

    if (!adjacencyList.has(source)) {
      adjacencyList.set(source, []);
    }
    adjacencyList.get(source).push(destination);
  });

  const queue = Array.from(nodesMap.keys()).filter(key => ![...adjacencyList.values()].flatMap(v => v).includes(key));
  queue.forEach(source => levelsMap.set(source, 0));

  while (queue.length > 0) {
    const current = queue.shift();
    const currentLevel = levelsMap.get(current);
    const neighbors = adjacencyList.get(current) || [];

    neighbors.forEach(neighbor => {
      if (!levelsMap.has(neighbor) || levelsMap.get(neighbor) > currentLevel + 1) {
        levelsMap.set(neighbor, currentLevel + 1);
        queue.push(neighbor);
      }
    });
  }

  const HORIZONTAL_GAP = 300;
  const VERTICAL_GAP = 150;
  const levelIndices = {};

  Array.from(nodesMap.entries()).forEach(([name, node]) => {
    const level = levelsMap.get(name);
    levelIndices[level] = levelIndices[level] || 0;
    node.position = {
      x: level * HORIZONTAL_GAP,
      y: levelIndices[level] * VERTICAL_GAP + VERTICAL_GAP
    };
    levelIndices[level] += 1;
  });

  return { nodes: Array.from(nodesMap.values()), edges };
};
