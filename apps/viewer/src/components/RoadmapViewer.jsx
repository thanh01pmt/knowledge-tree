import { useState, useEffect, useCallback } from 'react';
import RoadmapFlow3D from './RoadmapFlow3D';
import './RoadmapViewer.css';

export default function RoadmapViewer() {
  const [roadmaps, setRoadmaps] = useState([]);
  const [selectedRoadmap, setSelectedRoadmap] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [viewMode, setViewMode] = useState('3d'); // '3d' | 'timeline' | 'detail'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showFileInput, setShowFileInput] = useState(false);
  const [visualConfig, setVisualConfig] = useState({});
  const [levelConfig, setLevelConfig] = useState({});

  // Load roadmaps on mount
  useEffect(() => {
    loadAvailableRoadmaps();
  }, []);

  const loadAvailableRoadmaps = async () => {
    try {
      const manifest = localStorage.getItem('roadmap_manifest');
      if (manifest) {
        const parsed = JSON.parse(manifest);
        setRoadmaps(parsed);
        if (parsed.length > 0 && !selectedRoadmap) {
          setSelectedRoadmap(parsed[0]);
        }
      } else {
        await loadPublicRoadmaps();
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const loadPublicRoadmaps = async () => {
    try {
      const knownRoadmaps = [
        { path: '/roadmaps/rust-cli.json', code: 'RUST_CLI_001' },
        { path: '/roadmaps/portfolio-js.json', code: 'PORTFOLIO_GAME' },
        { path: '/roadmaps/jit-quiz.json', code: 'JIT_QUIZ' }
      ];
      const loaded = [];
      for (const rm of knownRoadmaps) {
        try {
          const resp = await fetch(rm.path);
          if (resp.ok) {
            const data = await resp.json();
            loaded.push(data);
            const key = `roadmap_${data.project_brief?.project_code || rm.code}`;
            localStorage.setItem(key, JSON.stringify(data));
          }
        } catch (e) {
          console.warn(`Failed to load ${rm.path}:`, e);
        }
      }
      if (loaded.length > 0) {
        setRoadmaps(loaded);
        const manifest = loaded.map(m => ({
          project_code: m.project_brief?.project_code,
          title: m.project_brief?.title,
          created_at: new Date().toISOString(),
          key: `roadmap_${m.project_brief?.project_code}`
        }));
        localStorage.setItem('roadmap_manifest', JSON.stringify(manifest));
        if (!selectedRoadmap) {
          setSelectedRoadmap(loaded[0]);
        }
      }
    } catch (err) {
      console.warn('Failed to load public roadmaps:', err);
    }
  };

  const handleFileLoad = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const roadmap = JSON.parse(event.target.result);
        const key = `roadmap_${roadmap.project_brief?.project_code || Date.now()}`;
        localStorage.setItem(key, JSON.stringify(roadmap));
        
        const manifest = localStorage.getItem('roadmap_manifest');
        const manifests = manifest ? JSON.parse(manifest) : [];
        if (!manifests.find(m => m.project_brief?.project_code === roadmap.project_brief?.project_code)) {
          manifests.push({
            project_code: roadmap.project_brief?.project_code,
            title: roadmap.project_brief?.title,
            created_at: new Date().toISOString(),
            key
          });
          localStorage.setItem('roadmap_manifest', JSON.stringify(manifests));
        }
        loadAvailableRoadmaps();
        setSelectedRoadmap(roadmap);
      } catch (err) {
        setError(`Invalid JSON: ${err.message}`);
      } finally {
        setLoading(false);
        setShowFileInput(false);
      }
    };
    reader.readAsText(file);
  };

  const handleNodeSelect = useCallback((node) => {
    setSelectedNode(node);
  }, []);

  if (loading) {
    return (
      <div className="roadmap-viewer loading">
        <div className="spinner"></div>
        <p>Loading roadmap...</p>
      </div>
    );
  }

  return (
    <div className="roadmap-viewer">
      <header className="viewer-header">
        <h1>🗺️ Roadmap Flow 3D</h1>
        <div className="header-actions">
          <input 
            type="file" 
            accept=".json" 
            onChange={handleFileLoad} 
            className="file-input"
            id="roadmap-file"
            style={{ display: showFileInput ? 'block' : 'none' }}
          />
          <label htmlFor="roadmap-file" className="btn btn-primary" onClick={() => setShowFileInput(true)}>
            📁 Load Roadmap JSON
          </label>
          {roadmaps.length > 0 && (
            <select 
              value={selectedRoadmap?.project_brief?.project_code || ''} 
              onChange={(e) => {
                const rm = roadmaps.find(r => r.project_brief?.project_code === e.target.value);
                if (rm) setSelectedRoadmap(rm);
              }}
              className="btn btn-secondary"
            >
              <option value="">Select Roadmap...</option>
              {roadmaps.map(r => (
                <option key={r.project_brief?.project_code} value={r.project_brief?.project_code}>
                  {r.project_brief?.title} ({r.project_brief?.project_code})
                </option>
              ))}
            </select>
          )}
        </div>
      </header>

      {error && <div className="error-banner">⚠️ {error}</div>}

      {!selectedRoadmap ? (
        <RoadmapList roadmaps={roadmaps} onSelect={setSelectedRoadmap} />
      ) : viewMode === '3d' ? (
        <div className="view-3d-container">
          <RoadmapFlow3D
            roadmap={selectedRoadmap}
            onNodeSelect={handleNodeSelect}
            selectedNodeId={selectedNode?.id}
            visualConfig={visualConfig}
            levelConfig={levelConfig}
          />
        </div>
      ) : viewMode === 'timeline' ? (
        <TimelineView 
          roadmap={selectedRoadmap}
          onModeChange={setViewMode}
        />
      ) : (
        <DetailView 
          roadmap={selectedRoadmap}
          onModeChange={setViewMode}
        />
      )}

      {selectedNode && (
        <NodeSidePanel 
          node={selectedNode} 
          roadmap={selectedRoadmap}
          onClose={() => setSelectedNode(null)}
        />
      )}
    </div>
  );
}

function RoadmapList({ roadmaps, onSelect }) {
  return (
    <div className="roadmap-list-view">
      {roadmaps.length === 0 ? (
        <div className="empty-state">
          <h2>No Roadmaps Found</h2>
          <p>Click "Load Roadmap JSON" to load a roadmap generated by the Curriculum Agent OS.</p>
          <p className="hint">Roadmaps are saved to localStorage after loading.</p>
        </div>
      ) : (
        <div className="roadmap-grid">
          {roadmaps.map(rm => (
            <div key={rm.key || rm.project_code} className="roadmap-card" onClick={() => onSelect(rm)}>
              <div className="card-header">
                <h3>{rm.project_brief?.title || rm.title}</h3>
                <span className="project-code">{rm.project_brief?.project_code || rm.project_code}</span>
              </div>
              <div className="card-meta">
                <span>📦 {rm.project_brief?.tech_stack?.join(', ') || 'N/A'}</span>
                <span>🎯 {rm.waterfall_phases?.length || 0} phases</span>
                <span>⏱️ {rm.user_profile?.total_budget_hours || 0}h total</span>
              </div>
              <div className="card-status">
                <span className={`status ${rm.student_active_roadmap?.status?.toLowerCase()?.replace('_', '-') || 'unknown'}`}>
                  {rm.student_active_roadmap?.status || 'UNKNOWN'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function TimelineView({ roadmap, onModeChange }) {
  if (!roadmap) return <div className="empty-state">No roadmap selected</div>;
  
  const phases = roadmap.waterfall_phases || [];
  const gates = roadmap.waterfall_gates || [];

  return (
    <div className="timeline-view">
      <div className="view-toolbar">
        <h2>📅 Timeline / Waterfall</h2>
        <div className="toolbar-actions">
          <button className="btn btn-outline" onClick={() => onModeChange('3d')}>🌐 3D Flow</button>
          <button className="btn btn-outline" onClick={() => onModeChange('detail')}>📋 Detail</button>
        </div>
      </div>
      <div className="timeline-container">
        {phases.map((phase, idx) => {
          const gate = gates[idx];
          return (
            <div key={phase.phase_num} className="timeline-phase">
              <div className="phase-header">
                <span className="phase-number">Phase {phase.phase_num}</span>
                <h3 className="phase-title">{phase.title}</h3>
                <span className="phase-timeframe">{phase.timeframe}</span>
              </div>
              <div className="phase-action"><code>{phase.engineering_action}</code></div>
              <div className="phase-prereq">Prereq: <em>{phase.required_prereq_knowledge}</em></div>
              <div className="phase-concepts">
                {phase.matching_concept_codes?.map(c => <span key={c} className="concept-tag">{c}</span>)}
              </div>
              {gate && (
                <div className="phase-gate">
                  <strong>⛔ Gate {idx}: </strong>{gate.checkpoint} — <span className="gate-status">{gate.status}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function DetailView({ roadmap, onModeChange }) {
  if (!roadmap) return <div className="empty-state">No roadmap selected</div>;

  return (
    <div className="detail-view">
      <div className="view-toolbar">
        <h2>📋 Project Details</h2>
        <div className="toolbar-actions">
          <button className="btn btn-outline" onClick={() => onModeChange('3d')}>🌐 3D Flow</button>
          <button className="btn btn-outline" onClick={() => onModeChange('timeline')}>📅 Timeline</button>
        </div>
      </div>
      <div className="detail-grid">
        <section className="detail-section">
          <h3>📌 Project Brief</h3>
          <dl>
            <dt>Title</dt><dd>{roadmap.project_brief?.title}</dd>
            <dt>Code</dt><dd>{roadmap.project_brief?.project_code}</dd>
            <dt>Type</dt><dd>{roadmap.project_brief?.type}</dd>
            <dt>Target Learner</dt><dd>{roadmap.project_brief?.target_learner}</dd>
            <dt>Tech Stack</dt><dd>{roadmap.project_brief?.tech_stack?.join(', ')}</dd>
            <dt>Key Features</dt>
            <dd><ul>{roadmap.project_brief?.key_features?.map(f => <li key={f}>{f}</li>)}</ul></dd>
          </dl>
        </section>
        
        <section className="detail-section">
          <h3>👤 Learner Profile</h3>
          <dl>
            <dt>Age Group</dt><dd>{roadmap.user_profile?.age_group}</dd>
            <dt>Focus Window</dt><dd>{roadmap.user_profile?.focus_window_minutes} min/task</dd>
            <dt>Weekly Hours</dt><dd>{roadmap.user_profile?.weekly_hours}h</dd>
            <dt>Target Weeks</dt><dd>{roadmap.user_profile?.target_weeks}w</dd>
            <dt>Total Budget</dt><dd>{roadmap.user_profile?.total_budget_hours}h</dd>
            <dt>Outcome</dt><dd>{roadmap.user_profile?.ultimate_outcome}</dd>
            <dt>Modality</dt><dd>{roadmap.user_profile?.preferred_modality}</dd>
            <dt>Known Concepts</dt><dd>{roadmap.user_profile?.known_concepts?.join(', ') || 'None'}</dd>
          </dl>
        </section>

        <section className="detail-section">
          <h3>⚙️ Tech Stack Advisor</h3>
          <dl>
            <dt>Chosen Option</dt><dd>{roadmap.techstack_advisor?.chosen_option}</dd>
            <dt>Estimated Effort</dt><dd>{roadmap.techstack_advisor?.estimated_effort_hours}h</dd>
            <dt>Learner Budget</dt><dd>{roadmap.techstack_advisor?.learner_budget_hours}h</dd>
            <dt>Build Tooling</dt><dd>{roadmap.techstack_advisor?.stack?.build_tooling}</dd>
            <dt>Trade-offs</dt>
            <dd><ul>{roadmap.techstack_advisor?.tradeoffs_noted?.map((t, i) => <li key={i}>{t}</li>)}</ul></dd>
          </dl>
        </section>

        <section className="detail-section">
          <h3>🏗️ Build Guide</h3>
          <div className="build-guide">
            {roadmap.step_by_step_build_guide?.map((step, i) => (
              <div key={i} className="build-step">
                <h4>Phase {step.phase_id}: {step.title}</h4>
                <p><strong>Action:</strong> {step.engineering_action}</p>
                <p><strong>Prereq:</strong> {step.required_prereq_knowledge}</p>
                <p><strong>Concepts:</strong> {step.matching_concept_codes?.join(', ')}</p>
              </div>
            ))}
          </div>
        </section>

        {roadmap.quarantine_candidates?.length > 0 && (
          <section className="detail-section quarantine">
            <h3>🔒 Quarantine Candidates ({roadmap.quarantine_candidates.length})</h3>
            {roadmap.quarantine_candidates.map((q, i) => (
              <div key={i} className="quarantine-item">
                <h4>{q.lo_id}</h4>
                <p><strong>Label:</strong> {q.label}</p>
                <p><strong>Verdict:</strong> {q.judge_verdict}</p>
                <p><strong>Prerequisites:</strong> {q.prerequisites?.join(', ')}</p>
                <p><strong>Pending Human Approval:</strong> {q.pending_human_approval ? '✅ Yes' : '❌ No'}</p>
              </div>
            ))}
          </section>
        )}

        <section className="detail-section">
          <h3>📈 Roadmap Graph Stats</h3>
          <dl>
            <dt>Nodes</dt><dd>{roadmap.roadmap_graph?.nodes?.length || 0}</dd>
            <dt>Edges</dt><dd>{roadmap.roadmap_graph?.edges?.length || 0}</dd>
            <dt>Topo Order</dt><dd>{roadmap.topo_order?.length || 0} concepts</dd>
            <dt>Waterfall Phases</dt><dd>{roadmap.waterfall_phases?.length || 0}</dd>
            <dt>Waterfall Gates</dt><dd>{roadmap.waterfall_gates?.length || 0}</dd>
          </dl>
        </section>
      </div>
    </div>
  );
}

function NodeSidePanel({ node, roadmap, onClose }) {
  const phase = roadmap?.waterfall_phases?.find(p => 
    p.matching_concept_codes?.includes(node.id.replace('concept-', '')) ||
    p.matching_concept_codes?.some(c => node.name.includes(c))
  );
  
  const gate = roadmap?.waterfall_gates?.find(g => 
    g.gate_id?.includes(node.id) || g.phase?.includes(node.name)
  );

  return (
    <div className="side-panel-overlay" onClick={onClose}>
      <div className="side-panel" onClick={e => e.stopPropagation()}>
        <div className="side-panel-header">
          <h3>{node.type === 'gate' ? '⛔' : node.type === 'phase' ? '📦' : node.type === 'feature' ? '⚙️' : '📚'} {node.name}</h3>
          <button className="side-panel-close" onClick={onClose}>×</button>
        </div>
        <div className="side-panel-content">
          <dl>
            <dt>ID</dt><dd>{node.id}</dd>
            <dt>Type</dt><dd>{node.type}</dd>
            <dt>Level</dt><dd>{node.level}</dd>
            {node.phaseNum && <><dt>Phase</dt><dd>{node.phaseNum}</dd></>}
            {node.estimatedHours && <><dt>Est. Hours</dt><dd>{node.estimatedHours}h</dd></>}
            {node.timeframe && <><dt>Timeframe</dt><dd>{node.timeframe}</dd></>}
          </dl>
          
          {node.description && (
            <div className="panel-section">
              <h4>Description</h4>
              <p>{node.description}</p>
            </div>
          )}
          
          {phase && (
            <div className="panel-section">
              <h4>📋 Phase Details</h4>
              <dl>
                <dt>Phase</dt><dd>{phase.phase_num}: {phase.title}</dd>
                <dt>Action</dt><dd>{phase.engineering_action}</dd>
                <dt>Timeframe</dt><dd>{phase.timeframe}</dd>
                <dt>Prereq Knowledge</dt><dd>{phase.required_prereq_knowledge}</dd>
                <dt>Concepts</dt><dd>{phase.matching_concept_codes?.join(', ')}</dd>
              </dl>
            </div>
          )}
          
          {gate && (
            <div className="panel-section">
              <h4>⛔ Gate Checkpoint</h4>
              <dl>
                <dt>Gate ID</dt><dd>{gate.gate_id}</dd>
                <dt>Checkpoint</dt><dd>{gate.checkpoint}</dd>
                <dt>Status</dt><dd>{gate.status}</dd>
                <dt>Remediation</dt><dd>{gate.remediation_sprint?.sprint_title}</dd>
              </dl>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}