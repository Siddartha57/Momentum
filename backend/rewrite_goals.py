import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

goals_replacement = '''export function Goals() {
  const { data: goals, refetch: refetchGoals, loading: goalsLoading } = useFetch<any[]>("/api/goals");
  const [selectedGoal, setSelectedGoal] = useState<number | null>(null);
  const { data: roadmap, refetch: refetchRoadmap, loading: roadmapLoading } = useFetch<any>(selectedGoal ? `/api/roadmaps/${selectedGoal}` : "");
  const [editingGoal, setEditingGoal] = useState<any | null>(null);
  const [conceptsInput, setConceptsInput] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  async function createGoal(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: fd.get("name"),
      description: fd.get("description"),
      category: fd.get("category"),
      start_date: fd.get("start_date"),
      end_date: fd.get("end_date"),
      priority: fd.get("priority"),
      daily_study_time: Number(fd.get("daily_study_time")),
      weekly_off_day: fd.get("weekly_off_day"),
      difficulty: fd.get("difficulty")
    };
    try {
      await api("/api/goals", { method: "POST", body: JSON.stringify(payload) });
      refetchGoals();
      (e.target as HTMLFormElement).reset();
      toast.success("Goal created! Let's build your roadmap.");
    } catch (err) {
      toast.error("Failed to create goal");
    }
  }

  async function updateStatus(id: number, status: string) {
    try {
      await api(`/api/goals/${id}/status?status_value=${status}`, { method: "PATCH" });
      refetchGoals();
      toast.success(`Goal ${status}`);
    } catch (err) {}
  }

  async function deleteGoal(id: number) {
    try {
      await api(`/api/goals/${id}`, { method: "DELETE" });
      refetchGoals();
      if (selectedGoal === id) setSelectedGoal(null);
      toast.success("Goal deleted");
    } catch (err) {}
  }

  async function saveEdit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: fd.get("name"),
      description: fd.get("description"),
      category: fd.get("category"),
      start_date: fd.get("start_date"),
      end_date: fd.get("end_date"),
      priority: fd.get("priority"),
      daily_study_time: Number(fd.get("daily_study_time")),
      weekly_off_day: fd.get("weekly_off_day"),
      difficulty: fd.get("difficulty")
    };
    try {
      await api(`/api/goals/${editingGoal.id}`, { method: "PUT", body: JSON.stringify(payload) });
      setEditingGoal(null);
      refetchGoals();
      toast.success("Goal updated");
    } catch (err) {}
  }

  async function generateRoadmap(e: FormEvent) {
    e.preventDefault();
    if (!selectedGoal || !conceptsInput.trim()) return;
    setIsGenerating(true);
    const concepts = conceptsInput.split('\\n').map(c => c.trim()).filter(c => c);
    try {
      await api(`/api/goals/${selectedGoal}/roadmap`, {
        method: "POST",
        body: JSON.stringify({ concepts })
      });
      await refetchRoadmap();
      setConceptsInput("");
      toast.success("Roadmap generated successfully!");
    } catch (err) {
      toast.error("Failed to generate roadmap");
    } finally {
      setIsGenerating(false);
    }
  }

  if (goalsLoading) return <Spinner message="Loading Goals..." />;

  return (
    <div className="space-y-6">
      <Header title="Goals & Roadmaps" action={`${goals?.length || 0} active goals`} />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="text-xl font-bold flex items-center gap-2"><Flame className="text-mint" /> Create Goal</h2>
          <form onSubmit={createGoal} className="mt-4 space-y-4">
            <input name="name" required placeholder="Goal Name" className="w-full rounded bg-white/5 border border-white/10 p-2" />
            <textarea name="description" placeholder="Description" className="w-full rounded bg-white/5 border border-white/10 p-2" />
            <div className="grid grid-cols-2 gap-4">
              <input name="start_date" type="date" required className="w-full rounded bg-white/5 border border-white/10 p-2" />
              <input name="end_date" type="date" required className="w-full rounded bg-white/5 border border-white/10 p-2" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <select name="category" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                <option value="Personal Development">Personal Development</option>
                <option value="Career">Career</option>
                <option value="Health">Health</option>
              </select>
              <select name="priority" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <input name="daily_study_time" type="number" step="0.5" defaultValue="1.0" required placeholder="Daily Hrs" className="w-full rounded bg-white/5 border border-white/10 p-2" />
              <select name="weekly_off_day" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                {["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"].map(d => <option key={d} value={d}>{d}</option>)}
              </select>
              <select name="difficulty" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <button className="w-full bg-mint text-ink font-bold py-2 rounded focus-ring flex justify-center items-center gap-2">
              Create Goal
            </button>
          </form>
        </Card>
        <div className="space-y-6">
          <Card>
            <h2 className="text-xl font-bold mb-4">Your Goals</h2>
            {(!goals || goals.length === 0) && <p className="text-white/50 text-sm">{getRandomMotivation()}</p>}
            {goals?.map(g => (
              <div key={g.id}>
                {editingGoal?.id === g.id ? (
                  <form onSubmit={saveEdit} className="p-3 mb-2 bg-white/5 rounded border border-mint/30 space-y-3">
                    <input name="name" required defaultValue={g.name} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                    <textarea name="description" defaultValue={g.description} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                    <div className="grid grid-cols-2 gap-3">
                      <input name="start_date" type="date" required defaultValue={g.start_date} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                      <input name="end_date" type="date" required defaultValue={g.end_date} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <select name="category" defaultValue={g.category} className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                        <option value="Personal Development">Personal Development</option>
                        <option value="Career">Career</option>
                        <option value="Health">Health</option>
                      </select>
                      <select name="priority" defaultValue={g.priority} className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                      </select>
                    </div>
                    <div className="flex justify-end gap-2 mt-2">
                      <button type="button" onClick={() => setEditingGoal(null)} className="text-white/50 text-sm">Cancel</button>
                      <button type="submit" className="text-mint font-bold text-sm">Save</button>
                    </div>
                  </form>
                ) : (
                  <div className={`p-4 mb-3 border rounded-lg transition-colors cursor-pointer ${selectedGoal === g.id ? 'bg-mint/10 border-mint/30' : 'bg-white/5 border-white/10 hover:border-white/20'}`} onClick={() => setSelectedGoal(g.id)}>
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold flex items-center gap-2">
                          {g.name}
                          {g.status === 'completed' && <Check size={14} className="text-mint" />}
                        </h3>
                        <p className="text-sm text-white/60 line-clamp-1">{g.description}</p>
                      </div>
                      <div className="flex gap-2">
                        <button onClick={(e) => { e.stopPropagation(); setEditingGoal(g); }} className="text-white/50 hover:text-white"><Edit3 size={16} /></button>
                        <button onClick={(e) => { e.stopPropagation(); deleteGoal(g.id); }} className="text-white/50 hover:text-coral"><Trash2 size={16} /></button>
                      </div>
                    </div>
                    <div className="flex justify-between text-xs mt-3">
                      <span className="bg-white/10 px-2 py-1 rounded">{g.category}</span>
                      <div className="flex gap-2">
                        {g.status === 'active' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'paused'); }} className="text-amber">Pause</button>}
                        {g.status === 'paused' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'active'); }} className="text-mint">Resume</button>}
                        {g.status !== 'completed' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'completed'); }} className="text-mint font-bold">Complete</button>}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </Card>

          {selectedGoal && (
            <Card>
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><ArrowRight className="text-mint" /> Roadmap Engine</h2>
              {roadmapLoading ? (
                <Spinner message="Loading Roadmap..." />
              ) : !roadmap ? (
                <div>
                  <p className="text-sm text-white/60 mb-4">No roadmap generated yet. List your main sub-goals or concepts below (one per line). We will allocate sub-timelines for each.</p>
                  <form onSubmit={generateRoadmap}>
                    <textarea 
                      value={conceptsInput} 
                      onChange={(e) => setConceptsInput(e.target.value)}
                      placeholder="e.g. Python\\nHTML\\nCSS\\nReact" 
                      className="w-full rounded bg-white/5 border border-white/10 p-3 h-32 text-sm font-mono mb-3 custom-scrollbar" 
                      required 
                    />
                    <button disabled={isGenerating} className="w-full bg-mint text-ink font-bold py-2 rounded focus-ring flex justify-center items-center gap-2">
                      {isGenerating ? <ButtonSpinner /> : "Build Animated Roadmap"}
                    </button>
                  </form>
                </div>
              ) : (
                <div className="space-y-6 relative pl-4 border-l-2 border-white/10">
                  {JSON.parse(roadmap.milestones_json).map((m: any, i: number) => (
                    <motion.div 
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="relative"
                    >
                      <div className="absolute -left-[25px] top-1 w-3 h-3 rounded-full bg-mint shadow-[0_0_10px_rgba(94,243,179,0.5)]" />
                      <div className="bg-white/5 border border-white/10 rounded-lg p-4 hover:border-mint/30 transition-colors">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-bold text-mint">{m.concept || m.title || `Phase ${i+1}`}</h4>
                          <span className="text-xs bg-white/10 px-2 py-1 rounded">Week {i+1}</span>
                        </div>
                        <p className="text-sm text-white/70">Connect daily tasks to this concept to see progress.</p>
                      </div>
                    </motion.div>
                  ))}
                  <div className="mt-4 p-4 bg-mint/10 text-mint text-sm rounded-lg">
                    <strong>Tip:</strong> Create daily tasks in the Tasks tab and mention these concepts to progress through your timeline!
                  </div>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}'''

match = re.search(r'export function Goals\(\) \{.*?(?=export function Tasks\(\) \{)', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), goals_replacement + '\n\n')

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
