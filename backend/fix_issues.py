import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Dashboard
dashboard_pattern = r'export function Dashboard\(\) \{.*?(?=export function Goals\(\) \{)'
dashboard_replacement = '''export function Dashboard() {
  const { data: analytics, loading: analyticsLoading } = useFetch<any>("/api/analytics");
  const { data: tasks, refetch: refetchTasks, loading: tasksLoading } = useFetch<any[]>(`/api/tasks?day=${new Date().toISOString().split("T")[0]}`);
  const { data: goals, loading: goalsLoading } = useFetch<any[]>("/api/goals");
  const { data: quote } = useFetch<{ quote: string }>("/api/quotes/random");

  const [completingTask, setCompletingTask] = useState<number | null>(null);
  const [attachment, setAttachment] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  async function completeTaskFlow(e: FormEvent) {
    e.preventDefault();
    if (!completingTask) return;
    try {
      await api(`/api/tasks/${completingTask}/complete`, { 
        method: "PATCH",
        body: JSON.stringify({ attachment_data: attachment })
      });
      refetchTasks();
      setCompletingTask(null);
      setAttachment(null);
      setFileName(null);
      toast.success("Task completed! Momentum +1");
    } catch (e) { toast.error("Failed to complete task"); }
  }

  function handleFile(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => setAttachment(event.target?.result as string);
    reader.readAsDataURL(file);
  }

  if (analyticsLoading || tasksLoading || goalsLoading) return <Spinner message="Loading Dashboard..." />;

  const chartData = analytics?.daily_study_hours?.map((d: any) => ({
    day: new Date(d.date).toLocaleDateString('en-US', { weekday: 'short' }),
    hours: d.hours
  })) || [];

  const activeTasks = tasks?.filter(t => t.status !== 'completed')?.length || 0;
  const activeGoals = goals?.filter(g => g.status === 'active')?.length || 0;

  return (
    <div className="space-y-6 relative">
      <Header title="Today" action={quote?.quote || "Discipline equals freedom."} />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Current streak" value={`${analytics?.streak?.current || 0} days`} />
        <StatCard label="Best streak" value={`${analytics?.streak?.longest || 0} days`} tone="amber" />
        <StatCard label="Accountability" value={analytics?.accountability?.score || 0} tone="sky" />
        <StatCard label="Grace days" value={`${analytics?.grace_days_remaining || 0} left`} tone="coral" />
      </div>
      
      <div className="grid gap-4 xl:grid-cols-3">
        <Card className="col-span-1 xl:col-span-2">
          <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><Flame className="text-mint" /> Overview & Progress</h2>
          <div className="grid gap-4 grid-cols-2 md:grid-cols-3 mb-6">
            <div className="p-4 bg-white/5 rounded-lg border border-white/10 text-center">
              <p className="text-xs sm:text-sm text-white/50 uppercase tracking-wider mb-1">Total Goals</p>
              <p className="text-2xl sm:text-3xl font-black text-mint">{goals?.length || 0}</p>
            </div>
            <div className="p-4 bg-white/5 rounded-lg border border-white/10 text-center">
              <p className="text-xs sm:text-sm text-white/50 uppercase tracking-wider mb-1">Active Tasks</p>
              <p className="text-2xl sm:text-3xl font-black text-sky-400">{activeTasks}</p>
            </div>
            <div className="col-span-2 md:col-span-1 p-4 bg-white/5 rounded-lg border border-white/10 text-center">
              <p className="text-xs sm:text-sm text-white/50 uppercase tracking-wider mb-1">All-Time Hours</p>
              <p className="text-2xl sm:text-3xl font-black text-amber-400">{analytics?.daily_study_hours?.reduce((a:number, b:any)=>a+b.hours,0) || 0}h</p>
            </div>
          </div>
          <h3 className="text-lg font-bold mb-4">30-Day Study Progress</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="hours" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#5ef3b3" stopOpacity={0.65} />
                    <stop offset="95%" stopColor="#5ef3b3" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,.08)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,.45)" />
                <YAxis stroke="rgba(255,255,255,.45)" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1b26', borderColor: '#ffffff20', color: '#fff' }} itemStyle={{ color: '#5ef3b3' }} />
                <Area type="monotone" dataKey="hours" stroke="#5ef3b3" fill="url(#hours)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
        
        <Card className="col-span-1 flex flex-col min-h-[400px]">
          <h2 className="text-xl font-bold flex items-center gap-2"><ListTodo className="text-sky-400" /> Today's Focus</h2>
          {!tasks || tasks.length === 0 ? (
            <div className="flex-1 grid place-items-center mt-5">
              <p className="text-sm text-white/50 text-center">{getRandomMotivation()}</p>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto mt-4 space-y-3 custom-scrollbar">
              {tasks.map((task) => (
                <div key={task.id} className={`flex items-center gap-3 rounded-lg bg-white/5 border border-white/10 p-3 transition ${task.status === 'completed' ? 'opacity-50' : 'hover:bg-white/10'}`}>
                  <button 
                    onClick={() => task.status !== 'completed' && setCompletingTask(task.id)}
                    className={`grid h-5 w-5 place-items-center rounded border ${task.status === 'completed' ? 'border-mint bg-mint text-ink' : 'border-white/30'}`}
                  >
                    {task.status === 'completed' && <Check size={14} />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <p className={`truncate ${task.status === 'completed' ? 'line-through text-white/50' : ''}`}>{task.name}</p>
                    {task.concept && <p className="text-xs text-white/50 mt-1">{task.concept}</p>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {completingTask && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-ink border border-white/10 p-6 rounded-xl w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Complete Task</h3>
              <button onClick={() => { setCompletingTask(null); setAttachment(null); setFileName(null); }} className="text-white/50 hover:text-white"><X size={20}/></button>
            </div>
            <p className="text-white/70 mb-6 text-sm">Great job! Would you like to upload any files or evidence for this task before completing?</p>
            <form onSubmit={completeTaskFlow} className="space-y-4">
              <div className="border-2 border-dashed border-white/20 rounded-lg p-6 text-center hover:border-mint/50 transition-colors cursor-pointer relative bg-white/5">
                <input type="file" onChange={handleFile} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                <Upload className="mx-auto text-white/40 mb-2" />
                {fileName ? (
                  <p className="text-sm font-bold text-mint">{fileName}</p>
                ) : (
                  <p className="text-sm text-white/70">Click or drag file to attach (optional)</p>
                )}
              </div>
              <button className="w-full bg-mint text-ink font-bold py-3 rounded-lg flex items-center justify-center gap-2 hover:bg-mint/90 focus-ring">
                <Check size={18}/> Mark as Completed
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
}'''
content = re.sub(dashboard_pattern, dashboard_replacement + '\n\n', content, flags=re.DOTALL)

# 2. Fix Goals (roadmap JSON parse)
goals_pattern = r'const concepts = conceptsInput\.split.*?JSON\.parse\(roadmap\.milestones_json\)\.map'
goals_repl = r'''const concepts = conceptsInput.split('\\n').map(c => c.trim()).filter(c => c);
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

  const milestonesData = roadmap?.milestones ? (typeof roadmap.milestones === 'string' ? JSON.parse(roadmap.milestones) : roadmap.milestones) : [];

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
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
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
                      <div className="flex gap-2 flex-wrap">
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
              ) : !roadmap || milestonesData.length === 0 ? (
                <div>
                  <p className="text-sm text-white/60 mb-4">No roadmap generated yet. List your main sub-goals or concepts below (one per line). We will allocate sub-timelines for each.</p>
                  <form onSubmit={generateRoadmap}>
                    <textarea 
                      value={conceptsInput} 
                      onChange={(e) => setConceptsInput(e.target.value)}
                      placeholder="e.g. Python\\nHTML\\nCSS\\nReact" 
                      className="w-full rounded bg-white/5 border border-white/10 p-3 h-32 text-sm font-mono mb-3 custom-scrollbar focus-ring" 
                      required 
                    />
                    <button disabled={isGenerating} className="w-full bg-mint text-ink font-bold py-2 rounded focus-ring flex justify-center items-center gap-2">
                      {isGenerating ? <ButtonSpinner /> : "Build Animated Roadmap"}
                    </button>
                  </form>
                </div>
              ) : (
                <div className="space-y-6 relative pl-4 border-l-2 border-white/10">
                  {milestonesData.map'''

content = re.sub(goals_pattern, goals_repl, content, flags=re.DOTALL)

# 3. Fix Tasks
tasks_pattern = r'export function Tasks\(\) \{.*?(?=export function Analytics\(\) \{)'
tasks_replacement = '''export function Tasks() {
  const [tab, setTab] = useState<'daily'|'history'>('daily');
  const [filterDate, setFilterDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const { data: dailyTasks, refetch: refetchDaily, loading: dailyLoading } = useFetch<any[]>(`/api/tasks?day=${filterDate}`);
  const { data: allTasks, refetch: refetchAll, loading: allLoading } = useFetch<any[]>("/api/tasks");
  const { data: goals } = useFetch<any[]>("/api/goals");
  const [completingTask, setCompletingTask] = useState<number | null>(null);
  const [attachment, setAttachment] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const ITEMS_PER_PAGE = 10;

  const tasks = tab === 'daily' ? dailyTasks : allTasks?.filter(t => t.status === 'completed');
  const totalPages = Math.ceil((tasks?.length || 0) / ITEMS_PER_PAGE);
  const paginatedTasks = tab === 'history' ? tasks?.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE) : tasks;

  async function completeTaskFlow(e: FormEvent) {
    e.preventDefault();
    if (!completingTask) return;
    try {
      await api(`/api/tasks/${completingTask}/complete`, { 
        method: "PATCH",
        body: JSON.stringify({ attachment_data: attachment })
      });
      refetchDaily();
      refetchAll();
      setCompletingTask(null);
      setAttachment(null);
      setFileName(null);
      toast.success("Task completed! Momentum +1");
    } catch (e) { toast.error("Failed to complete task"); }
  }

  async function deleteTask(id: number) {
    try {
      await api(`/api/tasks/${id}`, { method: "DELETE" });
      refetchDaily();
      refetchAll();
      toast.success("Task deleted");
    } catch (e) { }
  }

  async function createTask(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: fd.get("name"),
      date: fd.get("date"),
      concept: fd.get("concept"),
      estimated_duration: Number(fd.get("estimated_duration"))
    };
    try {
      await api("/api/tasks", { method: "POST", body: JSON.stringify(payload) });
      refetchDaily();
      refetchAll();
      (e.target as HTMLFormElement).reset();
      toast.success("Task added!");
    } catch (e) { toast.error("Failed to add task"); }
  }

  function handleFile(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => setAttachment(event.target?.result as string);
    reader.readAsDataURL(file);
  }

  const groupedTasks = (paginatedTasks || []).reduce((acc: any, task: any) => {
    const concept = task.concept || "General";
    if (!acc[concept]) acc[concept] = [];
    acc[concept].push(task);
    return acc;
  }, {});

  return (
    <div className="space-y-6 relative">
      <Header title="Tasks" action="Session overview" />
      <Card>
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
          <div className="flex gap-4">
            <h2 className={`text-xl font-bold flex items-center gap-2 cursor-pointer ${tab === 'daily' ? 'text-mint' : 'text-white/50'}`} onClick={() => setTab('daily')}>
              <ListTodo size={20} /> Daily Tasks
            </h2>
            <h2 className={`text-xl font-bold flex items-center gap-2 cursor-pointer ${tab === 'history' ? 'text-mint' : 'text-white/50'}`} onClick={() => { setTab('history'); setPage(1); }}>
              <BookOpen size={20} /> History
            </h2>
          </div>
          {tab === 'daily' && (
            <input type="date" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} className="bg-white/5 border border-white/10 rounded p-2 text-sm focus-ring w-full sm:w-auto" />
          )}
        </div>
        
        {tab === 'daily' && (
          <form onSubmit={createTask} className="flex gap-3 mb-6 p-3 rounded-lg bg-white/5 border border-white/10 flex-col sm:flex-row flex-wrap">
            <input name="name" required placeholder="Task name" className="flex-1 min-w-[200px] rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <select name="concept" className="w-full sm:w-40 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring text-white">
              <option value="">Concept (Goal)...</option>
              {goals?.map(g => <option key={g.id} value={g.name}>{g.name}</option>)}
              <option value="General">General</option>
            </select>
            <input name="date" type="date" required defaultValue={filterDate} className="w-full sm:w-auto rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <div className="flex gap-2 w-full sm:w-auto">
              <input name="estimated_duration" type="number" step="0.25" defaultValue="1" required placeholder="Hours" className="w-20 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
              <button className="bg-mint text-ink font-bold px-4 py-2 rounded text-sm flex-1 sm:flex-none flex items-center justify-center gap-1 hover:bg-mint/80 transition-colors"><Plus size={16} /> Add</button>
            </div>
          </form>
        )}

        {(dailyLoading && tab === 'daily') || (allLoading && tab === 'history') ? (
          <Spinner message="Loading Tasks..." />
        ) : (!paginatedTasks || paginatedTasks.length === 0) ? (
          <p className="text-white/50 py-10 text-center">{getRandomMotivation()}</p>
        ) : (
          <div className="space-y-6">
            {Object.entries(groupedTasks).map(([concept, conceptTasks]: [string, any]) => (
              <div key={concept}>
                <h3 className="text-sm font-bold text-white/60 uppercase tracking-widest mb-3 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-mint"></div> {concept}
                </h3>
                <div className="space-y-3">
                  {conceptTasks.map((t: any) => (
                    <div key={t.id} className={`flex items-start sm:items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10 transition-opacity ${t.status === 'completed' && tab === 'daily' ? 'opacity-40' : ''}`}>
                      <div className="flex items-start sm:items-center gap-4">
                        {tab === 'daily' && (
                          <button onClick={() => t.status !== 'completed' && setCompletingTask(t.id)} className={`mt-1 sm:mt-0 grid h-6 w-6 place-items-center rounded-full border transition-colors ${t.status === 'completed' ? 'border-mint bg-mint text-ink' : 'border-white/20 hover:border-mint'}`}>
                            {t.status === 'completed' && <Check size={14} />}
                          </button>
                        )}
                        <div>
                          <p className={`font-bold ${t.status === 'completed' && tab === 'daily' ? 'line-through text-white/50' : ''}`}>{t.name}</p>
                          <div className="flex flex-wrap items-center gap-3 text-xs text-white/50 mt-1">
                            <span>Est: {t.estimated_duration}h</span>
                            {t.attachment_data && (
                              <a href={t.attachment_data} download={`attachment_${t.id}`} className="flex items-center gap-1 text-sky hover:underline" onClick={e => e.stopPropagation()}>
                                <Upload size={12}/> Download File
                              </a>
                            )}
                            {tab === 'history' && <span>Completed on: {t.date}</span>}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <span className="text-xs px-2 py-1 rounded bg-white/10 uppercase tracking-wide hidden sm:block">{t.status}</span>
                        <button onClick={() => deleteTask(t.id)} className="text-xs bg-coral/20 text-coral px-2 py-1 rounded hover:bg-coral/30"><Trash2 size={14} /></button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
        
        {tab === 'history' && totalPages > 1 && (
          <div className="flex justify-center items-center gap-4 mt-8">
            <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Previous</button>
            <span className="text-sm text-white/50">Page {page} of {totalPages}</span>
            <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Next</button>
          </div>
        )}
      </Card>

      {completingTask && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-ink border border-white/10 p-6 rounded-xl w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Complete Task</h3>
              <button onClick={() => { setCompletingTask(null); setAttachment(null); setFileName(null); }} className="text-white/50 hover:text-white"><X size={20}/></button>
            </div>
            <p className="text-white/70 mb-6 text-sm">Great job! Would you like to upload any files or evidence for this task before completing?</p>
            <form onSubmit={completeTaskFlow} className="space-y-4">
              <div className="border-2 border-dashed border-white/20 rounded-lg p-6 text-center hover:border-mint/50 transition-colors cursor-pointer relative bg-white/5">
                <input type="file" onChange={handleFile} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                <Upload className="mx-auto text-white/40 mb-2" />
                {fileName ? (
                  <p className="text-sm font-bold text-mint">{fileName}</p>
                ) : (
                  <p className="text-sm text-white/70">Click or drag file to attach (optional)</p>
                )}
              </div>
              <button className="w-full bg-mint text-ink font-bold py-3 rounded-lg flex items-center justify-center gap-2 hover:bg-mint/90 focus-ring">
                <Check size={18}/> Mark as Completed
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
}'''
content = re.sub(tasks_pattern, tasks_replacement + '\n\n', content, flags=re.DOTALL)


# 4. Fix Calendar & Journal
cal_journ_pattern = r'export function Calendar\(\) \{.*?(?=export function Pomodoro\(\) \{)'
cal_journ_replacement = '''export function Calendar() {
  const { data: analytics, loading } = useFetch<any>("/api/analytics");
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const { data: dayTasks, loading: tasksLoading } = useFetch<any[]>(selectedDate ? `/api/tasks?day=${selectedDate}` : "");
  const { data: journals, loading: journalsLoading } = useFetch<any[]>(`/api/journal`); 

  const cells = useMemo(() => {
    const logs = analytics?.daily_study_hours || [];
    const logMap = new Map(logs.map((l: any) => [l.date, l.hours]));
    const today = new Date();
    return Array.from({ length: 120 }, (_, i) => {
      const d = new Date(today);
      d.setDate(d.getDate() - (119 - i));
      const dateStr = d.toISOString().split("T")[0];
      const hours: number = (logMap.get(dateStr) as number) || 0;
      let tone = "bg-white/10 hover:bg-white/20";
      if (hours >= 4) tone = "bg-mint";
      else if (hours >= 2) tone = "bg-mint/60 hover:bg-mint/80";
      else if (hours > 0) tone = "bg-mint/30 hover:bg-mint/50";
      return { dateStr, tone, hours };
    });
  }, [analytics]);

  const selectedJournal = useMemo(() => {
    return journals?.find(j => j.date === selectedDate);
  }, [journals, selectedDate]);

  return (
    <div className="space-y-6">
      <Header title="Calendar Heatmap" action="Last 120 Days" />
      <Card>
        {loading ? <Spinner message="Loading Heatmap..." /> : (
          <div className="grid gap-1 sm:gap-2" style={{ gridTemplateColumns: "repeat(20, minmax(0, 1fr))" }}>
            {cells.map((cell, i) => (
              <div 
                key={i} 
                title={`${cell.dateStr}: ${cell.hours} hours`}
                onClick={() => setSelectedDate(cell.dateStr)}
                className={`h-4 sm:h-6 rounded cursor-pointer transition-transform hover:scale-110 ${cell.tone} ${selectedDate === cell.dateStr ? 'ring-2 ring-white ring-offset-2 ring-offset-ink' : ''}`} 
              />
            ))}
          </div>
        )}
      </Card>

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-6 md:grid-cols-2">
        {!selectedDate ? (
          <div className="md:col-span-2 p-10 text-center text-white/50 bg-white/5 rounded-lg border border-white/10">
            <p className="mb-2 text-lg">Select a day from the heatmap to view details.</p>
            <p className="text-sm italic">"{getRandomMotivation()}"</p>
          </div>
        ) : (
          <>
            <Card>
              <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><ListTodo className="text-mint" /> Tasks on {selectedDate}</h2>
              {tasksLoading ? <Spinner /> : !dayTasks || dayTasks.length === 0 ? (
                <p className="text-white/50">{getRandomMotivation()}</p>
              ) : (
                <div className="space-y-3">
                  {dayTasks.map(t => (
                    <div key={t.id} className="p-3 bg-white/5 border border-white/10 rounded flex justify-between items-center">
                      <div>
                        <p className={`font-bold ${t.status === 'completed' ? 'text-white/50 line-through' : ''}`}>{t.name}</p>
                        {t.concept && <p className="text-xs text-mint mt-1">{t.concept}</p>}
                      </div>
                      <span className="text-xs uppercase bg-white/10 px-2 py-1 rounded tracking-widest">{t.status}</span>
                    </div>
                  ))}
                </div>
              )}
            </Card>
            <Card>
              <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><BookOpen className="text-mint" /> Journal on {selectedDate}</h2>
              {journalsLoading ? <Spinner /> : !selectedJournal ? (
                <p className="text-white/50">No journal entry recorded for this day.</p>
              ) : (
                <div className="space-y-4">
                  <h3 className="font-bold text-lg text-mint">{selectedJournal.title}</h3>
                  <p className="text-sm text-white/80 whitespace-pre-wrap">{selectedJournal.notes}</p>
                  {selectedJournal.learnings && (
                    <div>
                      <strong className="text-xs text-white/50 uppercase tracking-widest block mb-1">Learnings</strong>
                      <p className="text-sm bg-white/5 p-2 rounded border border-white/10">{selectedJournal.learnings}</p>
                    </div>
                  )}
                  {selectedJournal.challenges && (
                    <div>
                      <strong className="text-xs text-white/50 uppercase tracking-widest block mb-1">Challenges</strong>
                      <p className="text-sm bg-coral/10 text-coral p-2 rounded border border-coral/20">{selectedJournal.challenges}</p>
                    </div>
                  )}
                  {selectedJournal.tomorrow_plan && (
                    <div>
                      <strong className="text-xs text-white/50 uppercase tracking-widest block mb-1">Tomorrow's Plan</strong>
                      <p className="text-sm bg-sky-400/10 text-sky-400 p-2 rounded border border-sky-400/20">{selectedJournal.tomorrow_plan}</p>
                    </div>
                  )}
                </div>
              )}
            </Card>
          </>
        )}
      </motion.div>
    </div>
  );
}

export function Journal() {
  const { data: entries, refetch, loading } = useFetch<any[]>("/api/journal");
  const [page, setPage] = useState(1);
  const ITEMS_PER_PAGE = 5;

  async function createJournal(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      entry_date: new Date().toISOString().split("T")[0],
      title: fd.get("title"),
      notes: fd.get("notes"),
      learnings: fd.get("learnings") || null,
      challenges: fd.get("challenges") || null,
      tomorrow_plan: fd.get("tomorrow_plan") || null,
    };
    try {
      await api("/api/journal", { method: "POST", body: JSON.stringify(payload) });
      refetch();
      (e.target as HTMLFormElement).reset();
      toast.success("Journal saved! Keep building momentum.");
    } catch (err) {
      toast.error("Failed to save journal");
    }
  }

  const totalPages = Math.ceil((entries?.length || 0) / ITEMS_PER_PAGE);
  const paginatedEntries = entries?.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  return (
    <div className="space-y-6">
      <Header title="Daily Journal" action={`${entries?.length || 0} total entries`} />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><BookOpen className="text-mint" /> New Entry</h2>
          <form onSubmit={createJournal} className="space-y-4">
            <input name="title" required placeholder="Entry Title" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <textarea name="notes" required placeholder="General notes about the day" className="w-full rounded bg-white/5 border border-white/10 p-2 min-h-[100px] focus-ring" />
            <textarea name="learnings" placeholder="What did you learn today?" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <textarea name="challenges" placeholder="Any challenges faced?" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <textarea name="tomorrow_plan" placeholder="Plan for tomorrow" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <button className="w-full bg-mint hover:bg-mint/90 text-ink font-bold py-2 rounded focus-ring transition-colors">Save Entry</button>
          </form>
        </Card>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Past Entries</h2>
          </div>
          {loading ? <Spinner message="Loading Journals..." /> : (!paginatedEntries || paginatedEntries.length === 0) ? (
            <p className="text-white/50">{getRandomMotivation()}</p>
          ) : (
            <>
              {paginatedEntries.map((entry) => (
                <Card key={entry.id}>
                  <p className="text-xs text-mint uppercase tracking-wide">{entry.date}</p>
                  <h3 className="text-lg font-bold mt-1">{entry.title}</h3>
                  <p className="mt-2 text-sm text-white/70 whitespace-pre-wrap">{entry.notes}</p>
                  {entry.tomorrow_plan && (
                    <div className="mt-3 bg-white/5 border border-white/10 rounded p-2">
                      <span className="text-xs text-white/50 uppercase tracking-widest block mb-1">Tomorrow's Plan</span>
                      <p className="text-sm text-mint">{entry.tomorrow_plan}</p>
                    </div>
                  )}
                </Card>
              ))}
              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-4 mt-6">
                  <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Previous</button>
                  <span className="text-sm text-white/50">Page {page} of {totalPages}</span>
                  <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Next</button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}'''
content = re.sub(cal_journ_pattern, cal_journ_replacement + '\n\n', content, flags=re.DOTALL)

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
