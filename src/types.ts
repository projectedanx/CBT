export interface ConceptNode {
  id: string;
  label: string;
  type: 'input-a' | 'input-b' | 'generic' | 'blend';
  group: number;
}

export interface ConceptLink {
  source: string;
  target: string;
  value: number;
}

export interface GraphData {
  nodes: ConceptNode[];
  links: ConceptLink[];
}

export interface GenericSpaceResult {
  commonStructure: string[];
  mappings: string[];
  similarityScore: number;
}

export interface BlendedConcept {
  name: string;
  description: string;
  detailedExplanation: string;
  rationale: string;
  noveltyScore: number;
  userRating?: 'like' | 'dislike';
}

export interface BlendResult {
  blends: BlendedConcept[];
  analysis: string;
}

export type AppState = 'idle' | 'analyzing' | 'blending' | 'complete' | 'error';

export interface HistoryItem {
  id: string;
  timestamp: number;
  conceptA: string;
  conceptB: string;
  genericSpace: GenericSpaceResult;
  blendResult: BlendResult;
  blendType: 'composition' | 'completion' | 'elaboration';
  isManualSave?: boolean;
}
