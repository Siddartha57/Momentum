import re

# ---- Fix Pages.tsx: Remove heatmap + quick actions from Dashboard ----
with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

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

  const chartData = analytics?.daily_study_hours?.slice(-30).map((d: any) => ({
    day: new Date(d.date).toLocaleDateString('en-US', { weekday: 'short' }),
    hours: d.hours
  })) || [];

  const activeTasks = tasks?.filter(t => t.status !== 'completed')?.length || 0;

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

match = re.search(r'export function Dashboard\(\) \{.*?(?=export function Goals\(\) \{)', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), dashboard_replacement + '\n\n')
    print("Dashboard replaced successfully")
else:
    print("ERROR: Dashboard pattern not found")

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Pages.tsx saved")
