import React from 'react';
import { Handle, Position } from 'reactflow';
import { GiWaterTank } from "react-icons/gi"; // Icon for SourceNode
import { FaHandHoldingWater, FaTrash } from "react-icons/fa";
import { FaFilter } from "react-icons/fa6";



// Source Node Component
const SourceNode = ({ data }) => (
  <div className="flex flex-col items-center justify-center w-32 h-20 bg-blue-50 border border-blue-300 rounded-lg shadow-sm text-center">
    <GiWaterTank className="text-blue-500 text-2xl mb-1" />
    <div className="text-xs text-blue-700">{data.label}</div>
    <Handle
      type="source"
      position={Position.Right}
      id="source-right" // Specific ID for the handle
      style={{ background: '#3182ce', width: 7, height: 7, borderRadius: '50%' }}
    />
  </div>
);

// Total Source Water Node Component
const Tanks = ({ data }) => (
  <div className="flex flex-col items-center justify-center w-32 h-20 bg-green-50 border border-green-300 rounded-lg shadow-sm text-center">
    <FaHandHoldingWater className="text-green-500 text-2xl mb-1" />
    <div className="text-xs text-green-700">{data.label}</div>
    {/* Handle for incoming connections */}
    <Handle
      type="target"
      position={Position.Left}
      id="total-left" // Specific ID for the handle
      style={{ background: '#38a169', width: 8, height: 8, borderRadius: '50%' }}
    />
    {/* Handle for outgoing connections to treatment */}
    <Handle
      type="source"
      position={Position.Right}
      id="total-right" // Specific ID for the handle
      style={{ background: '#38a169', width: 8, height: 8, borderRadius: '50%' }}
    />
  </div>
);

// Treatment Node Component
const TreatmentNode = ({ data }) => (
  <div className="flex flex-col items-center justify-center w-32 h-20 bg-purple-50 border border-purple-300 rounded-lg shadow-sm text-center">
    <FaFilter className="text-purple-500 text-2xl mb-1" />
    <div className="text-xs text-purple-700">{data.label}</div>
    {/* Handle for incoming water */}
    <Handle
      type="target"
      position={Position.Left}
      id="treatment-left" // Corrected to use label for consistency
      style={{ background: '#6d28d9', width: 7, height: 7, borderRadius: '50%' }}
    />
    {/* Handle for outgoing product water */}
    <Handle
      type="source"
      position={Position.Right}
      id="treatment-right" // Corrected to use label for consistency
      style={{ background: '#6d28d9', width: 7, height: 7, borderRadius: '50%' }}
    />
    {/* Handle for reject water, if needed */}
    <Handle
      type="source"
      position={Position.Bottom}
      id="treatment-bottom" // Corrected to use label for consistency
      style={{ background: '#6d28d9', width: 7, height: 7, borderRadius: '50%' }}
    />
  </div>
);

// Reject Water Node Component
const RejectNode = ({ data }) => (
  <div className="flex flex-col items-center justify-center w-32 h-20 bg-red-50 border border-red-300 rounded-lg shadow-sm text-center">
    <FaTrash className="text-red-500 text-2xl mb-1" />
    <div className="text-xs text-red-700">{data.label}</div>
    {/* Handle for incoming reject water */}
    <Handle
      type="target"
      position={Position.Top}
      id="reject-top" // Added specific ID for clarity
      style={{ background: '#e11d48', width: 7, height: 7, borderRadius: '50%' }}
    />
  </div>
);

export { SourceNode, Tanks, TreatmentNode, RejectNode };
