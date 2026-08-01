import { parseKnowledgeTree } from './src/utils/dataParser.js';

const rawData = {
  fields: [{ code: 'DAI', name: 'Data and Information' }],
  learning_objectives: [
    { code: 'ULO-1', concept_codes: 'C-1' },
    { code: 'CIO-1', parent_lo_code: 'ULO-1' },
    { code: 'SIO-1', parent_lo_code: 'CIO-1', concept_codes: 'C-1' } // Notice SIO has concept_codes!
  ],
  concepts: [{ code: 'C-1', topic_codes: 'T-1' }]
};

try {
  const result = parseKnowledgeTree(rawData);
  console.log("Nodes:", result.graphData.nodes.length);
  console.log("Links:", result.graphData.links.length);
  console.log("Links:", JSON.stringify(result.graphData.links));
} catch (e) {
  console.error("Error:", e);
}
