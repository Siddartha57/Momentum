with open('../frontend/src/pages/Pages.tsx', 'a', encoding='utf-8') as f:
    f.write('''

export function Header({ title, action }: { title: string; action?: ReactNode }) {
  return (
    <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
      <h1 className="text-3xl font-black">{title}</h1>
      {action && <div className="text-sm font-bold text-white/50">{action}</div>}
    </div>
  );
}

export function Achievements() {
  const { data: achievements } = useFetch<any[]>("/api/achievements");
  return (
    <div className="space-y-6">
      <Header title="Achievements" action={`${achievements?.filter(a => a.earned).length || 0} Unlocked`} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {badges.map((b) => {
          const earned = achievements?.find(a => a.name === b)?.earned;
          return (
            <Card key={b} className={`flex items-center gap-4 ${earned ? 'border-mint/30' : 'opacity-50'}`}>
              <div className={`grid h-12 w-12 place-items-center rounded-full ${earned ? 'bg-mint text-ink' : 'bg-white/10 text-white/50'}`}>
                <Trophy size={20} />
              </div>
              <div>
                <h3 className="font-bold">{b}</h3>
                <p className="text-xs text-white/50">{earned ? 'Unlocked' : 'Locked'}</p>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

export function Notifications() {
  const { data: notifications, refetch } = useFetch<any[]>("/api/notifications");
  async function markRead(id: number) {
    try {
      await api(`/api/notifications/${id}/read`, { method: "PATCH" });
      refetch();
    } catch (e) {}
  }
  return (
    <div className="space-y-6">
      <Header title="Notifications" action={`${notifications?.filter(n => !n.is_read).length || 0} Unread`} />
      <Card>
        {!notifications || notifications.length === 0 ? <p className="text-white/50">No notifications.</p> : (
          <div className="space-y-3">
            {notifications.map(n => (
              <div key={n.id} className={`p-4 rounded-lg border ${n.is_read ? 'bg-white/5 border-white/10 opacity-60' : 'bg-mint/10 border-mint/30 flex justify-between items-start'}`}>
                <div>
                  <h4 className="font-bold">{n.title}</h4>
                  <p className="text-sm text-white/70">{n.message}</p>
                </div>
                {!n.is_read && <button onClick={() => markRead(n.id)} className="text-xs text-mint">Mark Read</button>}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}

export function Settings() {
  const { data: settings, refetch } = useFetch<any>("/api/settings");
  async function toggleSetting(field: string, val: boolean) {
    try {
      await api("/api/settings", { method: "PUT", body: JSON.stringify({ [field]: val }) });
      refetch();
    } catch (e) {}
  }
  return (
    <div className="space-y-6">
      <Header title="Settings" action="Preferences" />
      <Card>
        <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><SettingsIcon className="text-mint" /> Preferences</h2>
        <div className="space-y-4">
          {['email_reminders', 'push_notifications', 'weekly_summary'].map((k) => (
            <div key={k} className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10">
              <span className="capitalize">{k.replace('_', ' ')}</span>
              <button 
                onClick={() => settings && toggleSetting(k, !settings[k])} 
                className={`w-12 h-6 rounded-full transition-colors ${settings?.[k] ? 'bg-mint' : 'bg-white/20'} relative`}
              >
                <div className={`absolute top-1 bg-white w-4 h-4 rounded-full transition-transform ${settings?.[k] ? 'left-7 bg-ink' : 'left-1'}`} />
              </button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
''')
