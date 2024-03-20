// initializeFlowchart.js

export const initializeFlowchart = (loadedSources, loadedTreatment) => {
  const sortedTreatment = loadedTreatment.sort(
    (a, b) => a.seq_number - b.seq_number
  );

  let totalInputWater = loadedSources.reduce(
    (sum, source) => sum + parseFloat(source.consumption),
    0
  );
  let nodes = [],
    edges = [];
  let treatmentXPosition = 600; // Initial X position for the first treatment node

  const verticalSpacing = 100; // Vertical spacing between nodes
  const sourcesYPositionStart = 25; // Starting Y position for source nodes
  const totalNodeYPosition =
    sourcesYPositionStart + ((loadedSources.length - 1) * verticalSpacing) / 2;

  const sourceNodes = loadedSources.map((source, index) => ({
    id: source.id.toString(),
    data: { label: source.name },
    position: { x: 100, y: sourcesYPositionStart + index * verticalSpacing },
    type: "sourceNode",
  }));

  const totalSourceWaterNode = {
    id: "total",
    data: {
      label: "Total Source Water",
      consumption: totalInputWater.toFixed(2),
    },
    position: { x: 400, y: totalNodeYPosition },
    type: "totalNode",
  };

  nodes.push(...sourceNodes, totalSourceWaterNode);

  sortedTreatment.forEach((treatment, index) => {
    const treatmentNodeId = `treatment-${treatment.id}`;
    nodes.push({
      id: treatmentNodeId,
      data: { label: treatment.name },
      position: { x: treatmentXPosition, y: 100 },
      type: "treatmentNode",
    });

    const sourceId =
      index === 0 ? "total" : `treatment-${sortedTreatment[index - 1].id}`;
    edges.push({
      id: `e${sourceId}-${treatmentNodeId}`,
      source: sourceId,
      target: treatmentNodeId,
      type: "waterEdge",
      data: {
        consumption:
          index === 0
            ? totalInputWater.toFixed(2)
            : sortedTreatment[index - 1].product_water,
      },
      animated: true,
    });

    const rejectWaterNodeId = `reject-${treatment.id}`;
    nodes.push({
      id: rejectWaterNodeId,
      data: { label: `Reject: ${treatment.reject_water} KL` },
      position: { x: treatmentXPosition, y: 250 },
      type: "rejectNode",
    });

    edges.push({
      id: `e${treatmentNodeId}-${rejectWaterNodeId}`,
      source: treatmentNodeId,
      sourceHandle: "treatment-bottom",
      target: rejectWaterNodeId,
      type: "waterEdge",
      data: { consumption: treatment.reject_water },
      animated: true,
    });

    treatmentXPosition += 250; // Increment X position for next treatment node
  });

  const sourceEdges = loadedSources.map((source) => ({
    id: `e${source.id}-total`,
    source: source.id.toString(),
    target: "total",
    type: "waterEdge",
    data: { consumption: source.consumption },
    animated: true,
  }));

  const lastTreatment = sortedTreatment[sortedTreatment.length - 1];
  const lastTreatmentNodeId = `treatment-${lastTreatment.id}`;

  // Create the final tank node
  const finalTankNodeId = "final-tank";
  const finalTankNode = {
    id: finalTankNodeId,
    data: {
      label: "Final Tank",
      consumption: lastTreatment.product_water + " KL",
    },
    position: { x: treatmentXPosition, y: 100 }, // Position to align or place suitably in the flow
    type: "totalNode", // Or create a new type 'finalTankNode' similar to 'totalNode' for styling
  };

  // Create an edge from the last treatment to the final tank
  const finalEdge = {
    id: `e${lastTreatmentNodeId}-${finalTankNodeId}`,
    source: lastTreatmentNodeId,
    target: finalTankNodeId,
    sourceHandle: "treatment-right", // Assuming the last treatment outputs from its right handle
    type: "waterEdge",
    data: { consumption: lastTreatment.product_water }, // Displaying product water into the tank
    animated: true,
  };

  // Add the final tank node and edge to the arrays
  nodes.push(finalTankNode);
  edges.push(finalEdge);

  edges.push(...sourceEdges);

  return { nodes, edges };
};
