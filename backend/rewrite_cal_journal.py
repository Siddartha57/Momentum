import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''export function Calendar() {
  const { data: analytics, loading } = useFetch<any>("/api/analytics");
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const { data: dayTasks, loading: tasksLoading } = useFetch<any[]>(selectedDate ? `/api/tasks?day=${selectedDate}` : "");
  const { data: journals, loading: journalsLoading } = useFetch<any[]>(`/api/journal`); // The API currently doesn't filter by date, so we fetch all and filter in frontend or we can use the selectedDate if we added it

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
    return journals?.find(j => j.entry_date === selectedDate);
  }, [journals, selectedDate]);

  return (
    <div className="space-y-6">
      <Header title="Calendar Heatmap" action="Last 120 Days" />
      <Card>
        {loading ? <Spinner message="Loading Heatmap..." /> : (
          <div className="grid gap-2" style={{ gridTemplateColumns: "repeat(20, minmax(0, 1fr))" }}>
            {cells.map((cell, i) => (
              <div 
                key={i} 
                title={`${cell.dateStr}: ${cell.hours} hours`}
                onClick={() => setSelectedDate(cell.dateStr)}
                className={`h-6 rounded cursor-pointer transition-transform hover:scale-110 ${cell.tone} ${selectedDate === cell.dateStr ? 'ring-2 ring-white ring-offset-2 ring-offset-ink' : ''}`} 
              />
            ))}
          </div>
        )}
      </Card>

      {selectedDate && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-6 md:grid-cols-2">
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
        </motion.div>
      )}
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
            <button className="w-full bg-mint text-ink font-bold py-2 rounded focus-ring">Save Entry</button>
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
                  <p className="text-xs text-mint uppercase tracking-wide">{entry.entry_date}</p>
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

match = re.search(r'export function Calendar\(\) \{.*?(?=export function Pomodoro\(\) \{)', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), replacement + '\n\n')

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
