import React, { useEffect, useState, useCallback, useRef } from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  applyNodeChanges,
} from "reactflow";
import "reactflow/dist/style.css";
import {
  SourceNode,
  Tanks,
  TreatmentNode,
  RejectNode,
} from "./Components/Node";
import WaterEdge from "./Components/WaterEdge";
import { initializeFlowchart } from "./initializeFlowchart";

const nodeTypes = {
  sourceNode: SourceNode,
  totalNode: Tanks,
  treatmentNode: TreatmentNode,
  rejectNode: RejectNode,
};

const edgeTypes = {
  waterEdge: WaterEdge,
};

function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const initialLayoutRef = useRef({ nodes: [], edges: [] }); // Store the initial layout

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  useEffect(() => {
    const sourceWaterFlow = window.sourceWaterFlow || [];
    const parsedData = typeof sourceWaterFlow === 'string' ? JSON.parse(sourceWaterFlow) : sourceWaterFlow;
    const { nodes: initializedNodes, edges: initializedEdges } =
      initializeFlowchart(parsedData);

    // Store the initial layout in a ref after initialization
    initialLayoutRef.current = {
      nodes: initializedNodes,
      edges: initializedEdges,
    };

    setNodes(initializedNodes);
    setEdges(initializedEdges);
  }, []);

  const resetLayout = useCallback(() => {
    // Reset nodes and edges to their initial state
    setNodes([...initialLayoutRef.current.nodes]);
    setEdges([...initialLayoutRef.current.edges]);
  }, []);

  return (
    <div
      style={{
        maxWidth: "100vw",
        height: "100vh",
        overflow: "hidden",
        background: "white",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <button
        className="bg-black text-white border rounded m-1 p-1"
        onClick={resetLayout}
        style={{ position: "absolute", zIndex: 1000 }}
      >
        Reset Layout
      </button>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        preventScrolling={false}
        onNodesChange={onNodesChange}
      >
        <MiniMap nodeStrokeWidth={3} fitView />
        <Controls position="top-right" />
        <Background variant="dots" gap={40} size={1} color="blue" />
      </ReactFlow>
    </div>
  );
}

export default App;
