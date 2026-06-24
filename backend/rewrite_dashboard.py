import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

dashboard_replacement = '''export function Dashboard() {
  const { data: analytics, loading: analyticsLoading } = useFetch<any>("/api/analytics");
  const { data: tasks, refetch: refetchTasks, loading: tasksLoading } = useFetch<any[]>(`/api/tasks?day=${new Date().toISOString().split("T")[0]}`);
  const { data: goals, loading: goalsLoading } = useFetch<any[]>("/api/goals");
  const { data: quote } = useFetch<{ quote: string }>("/api/quotes/random");

  async function completeTask(taskId: number) {
    try {
      await api(`/api/tasks/${taskId}/complete`, { method: "PATCH", body: "{}" }); // Added empty payload to avoid 422
      refetchTasks();
      toast.success("Task completed!");
    } catch (e) {
      toast.error("Failed to complete task.");
    }
  }

  if (analyticsLoading || tasksLoading || goalsLoading) return <Spinner message="Loading Dashboard..." />;

  const chartData = analytics?.daily_study_hours?.map((d: any) => ({
    day: new Date(d.date).toLocaleDateString('en-US', { weekday: 'short' }),
    hours: d.hours
  })) || [];

  const activeTasks = tasks?.filter(t => t.status !== 'completed')?.length || 0;
  const activeGoals = goals?.filter(g => g.status === 'active')?.length || 0;

  return (
    <div className="space-y-6">
      <Header title="Today" action={quote?.quote || "Discipline equals freedom."} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Current streak" value={`${analytics?.streak?.current || 0} days`} />
        <StatCard label="Best streak" value={`${analytics?.streak?.longest || 0} days`} tone="amber" />
        <StatCard label="Accountability" value={analytics?.accountability?.score || 0} tone="sky" />
        <StatCard label="Grace days" value={`${analytics?.grace_days_remaining || 0} left`} tone="coral" />
      </div>
      
      <div className="grid gap-4 xl:grid-cols-3">
        <Card className="col-span-1 xl:col-span-2">
          <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><Flame className="text-mint" /> Overview & Progress</h2>
          <div className="grid gap-4 md:grid-cols-3 mb-6">
            <div className="p-4 bg-white/5 rounded-lg border border-white/10 text-center">
              <p className="text-sm text-white/50 uppercase tracking-wider mb-1">Total Goals</p>
              <p className="text-3xl font-black text-mint">{goals?.length || 0}</p>
            </div>
            <div className="p-4 bg-white/5 rounded-lg border border-white/10 text-center">
              <p className="text-sm text-white/50 uppercase tracking-wider mb-1">Active Tasks</p>
              <p className="text-3xl font-black text-sky-400">{activeTasks}</p>
            </div>
            <div className="p-4 bg-white/5 rounded-lg border border-white/10 text-center">
              <p className="text-sm text-white/50 uppercase tracking-wider mb-1">All-Time Hours</p>
              <p className="text-3xl font-black text-amber-400">{analytics?.daily_study_hours?.reduce((a:number, b:any)=>a+b.hours,0) || 0}h</p>
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
                <Tooltip />
                <Area type="monotone" dataKey="hours" stroke="#5ef3b3" fill="url(#hours)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
        
        <Card className="col-span-1 flex flex-col">
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
                    onClick={() => task.status !== 'completed' && completeTask(task.id)}
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
    </div>
  );
}'''

match = re.search(r'export function Dashboard\(\) \{.*?(?=export function Goals\(\) \{)', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), dashboard_replacement + '\n\n')

# Check if Spinner imports are missing and add them
if 'Spinner' not in content:
    content = content.replace('import { usePomodoro } from "../context/PomodoroContext";', 'import { usePomodoro } from "../context/PomodoroContext";\nimport { Spinner, ButtonSpinner, getRandomMotivation } from "../components/ui";')

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
