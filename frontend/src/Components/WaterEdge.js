import React from "react";
import { getBezierPath, getMarkerEnd } from "reactflow";

const WaterEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data = {}, // Assuming `data` contains edge-specific information like `consumption`
  markerEndId,
}) => {
  const edgePath = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  }) || `M${sourceX},${sourceY} L${targetX},${targetY}`; // Fallback path for debugging

  const markerEnd = getMarkerEnd(markerEndId, "target");
  const centerX = (sourceX + targetX) / 2;
  const centerY = (sourceY + targetY) / 2;

  return (
    <>
      <path
        id={id}
        className="react-flow__edge-path"
        d={edgePath}
        markerEnd={markerEnd}
        fill="none"
        style= {{ stroke: "#74ccf4", strokeWidth: 4, strokeDasharray: "10" }}
      />
      <text
        x={centerX-5}
        y={centerY+10}
        style={{ fontSize: "12px", fill: "black", cursor: "default" }}
        dominantBaseline="middle"
        textAnchor="middle"
      >
        {data.consumption} KL
      </text>
    </>
  );
};

export default WaterEdge;
