import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

tasks_replacement = '''export function Tasks() {
  const [tab, setTab] = useState<'daily'|'history'>('daily');
  const [filterDate, setFilterDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const { data: dailyTasks, refetch: refetchDaily, loading: dailyLoading } = useFetch<any[]>(`/api/tasks?day=${filterDate}`);
  const { data: allTasks, refetch: refetchAll, loading: allLoading } = useFetch<any[]>("/api/tasks");
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
        <div className="flex justify-between items-center mb-6">
          <div className="flex gap-4">
            <h2 className={`text-xl font-bold flex items-center gap-2 cursor-pointer ${tab === 'daily' ? 'text-mint' : 'text-white/50'}`} onClick={() => setTab('daily')}>
              <ListTodo size={20} /> Daily Tasks
            </h2>
            <h2 className={`text-xl font-bold flex items-center gap-2 cursor-pointer ${tab === 'history' ? 'text-mint' : 'text-white/50'}`} onClick={() => { setTab('history'); setPage(1); }}>
              <BookOpen size={20} /> History
            </h2>
          </div>
          {tab === 'daily' && (
            <input type="date" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} className="bg-white/5 border border-white/10 rounded p-2 text-sm focus-ring" />
          )}
        </div>
        
        {tab === 'daily' && (
          <form onSubmit={createTask} className="flex gap-3 mb-6 p-3 rounded-lg bg-white/5 border border-white/10 flex-wrap">
            <input name="name" required placeholder="Task name" className="flex-1 min-w-[200px] rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <input name="concept" placeholder="Concept (optional)" className="w-40 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <input name="date" type="date" required defaultValue={filterDate} className="rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <input name="estimated_duration" type="number" step="0.25" defaultValue="1" required placeholder="Hours" className="w-24 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <button className="bg-mint text-ink font-bold px-4 py-2 rounded text-sm flex items-center gap-1 hover:bg-mint/80 transition-colors"><Plus size={16} /> Add</button>
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
                    <div key={t.id} className={`flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10 transition-opacity ${t.status === 'completed' && tab === 'daily' ? 'opacity-40' : ''}`}>
                      <div className="flex items-center gap-4">
                        {tab === 'daily' && (
                          <button onClick={() => t.status !== 'completed' && setCompletingTask(t.id)} className={`grid h-6 w-6 place-items-center rounded-full border transition-colors ${t.status === 'completed' ? 'border-mint bg-mint text-ink' : 'border-white/20 hover:border-mint'}`}>
                            {t.status === 'completed' && <Check size={14} />}
                          </button>
                        )}
                        <div>
                          <p className={`font-bold ${t.status === 'completed' && tab === 'daily' ? 'line-through text-white/50' : ''}`}>{t.name}</p>
                          <div className="flex items-center gap-3 text-xs text-white/50">
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
                      <div className="flex items-center gap-2">
                        <span className="text-xs px-2 py-1 rounded bg-white/10 uppercase tracking-wide">{t.status}</span>
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
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-ink border border-white/10 p-6 rounded-xl w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Complete Task</h3>
              <button onClick={() => { setCompletingTask(null); setAttachment(null); setFileName(null); }} className="text-white/50 hover:text-white"><X size={20}/></button>
            </div>
            <p className="text-white/70 mb-6">Great job! Would you like to upload any files or evidence for this task before completing?</p>
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

match = re.search(r'export function Tasks\(\) \{.*?(?=export function Analytics\(\) \{)', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), tasks_replacement + '\n\n')

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
