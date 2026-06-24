import re

# 1. Update backend/app/api/routes.py
routes_path = 'app/api/routes.py'
with open(routes_path, 'r', encoding='utf-8') as f:
    routes_content = f.read()

# Add PUT /me endpoint right after GET /me
me_put_code = '''
from pydantic import BaseModel
class UserUpdate(BaseModel):
    full_name: str | None = None
    daily_target_hours: float | None = None

@router.put("/me")
def update_me(payload: UserUpdate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> User:
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.daily_target_hours is not None:
        user.daily_target_hours = payload.daily_target_hours
    db.commit()
    return user
'''

if '@router.put("/me")' not in routes_content:
    routes_content = routes_content.replace(
        'def me(user: Annotated[User, Depends(current_user)]) -> User:\n    return user\n',
        'def me(user: Annotated[User, Depends(current_user)]) -> User:\n    return user\n' + me_put_code + '\n'
    )
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(routes_content)
    print("Updated routes.py")

# 2. Update frontend/src/pages/Pages.tsx
pages_path = '../frontend/src/pages/Pages.tsx'
with open(pages_path, 'r', encoding='utf-8') as f:
    pages_content = f.read()

settings_func = '''  async function updateProfile(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    try {
      await api("/api/me", { 
        method: "PUT", 
        body: JSON.stringify({ 
          full_name: fd.get("full_name"), 
          daily_target_hours: Number(fd.get("daily_target_hours")) 
        }) 
      });
      refetchProfile();
      toast.success("Profile updated successfully!");
    } catch (e) { toast.error("Failed to update profile"); }
  }'''

old_settings_func_pattern = r'async function updateProfile\(e: FormEvent<HTMLFormElement>\) \{.*?(?=  function logout\(\))'
pages_content = re.sub(old_settings_func_pattern, settings_func + '\n\n', pages_content, flags=re.DOTALL)

with open(pages_path, 'w', encoding='utf-8') as f:
    f.write(pages_content)
print("Updated Pages.tsx")

# 3. Update frontend/src/components/Layout.tsx
layout_path = '../frontend/src/components/Layout.tsx'
with open(layout_path, 'r', encoding='utf-8') as f:
    layout_content = f.read()

# Remove the center FAB from inside the nav
old_nav_pattern = r'\{/\* Center FAB - elevated above the nav bar \*/\}.*?(?=</nav>)'
layout_content = re.sub(old_nav_pattern, '', layout_content, flags=re.DOTALL)

# Add the center FAB outside the nav
new_mobile_fab = '''

      {/* ─── Mobile FAB (outside nav for z-index fix) ─── */}
      <div className="fixed left-1/2 -translate-x-1/2 bottom-8 z-50 flex flex-col items-center gap-2 lg:hidden">
        <AnimatePresence>
          {fabOpen && (
            <div className="absolute bottom-full mb-4 flex flex-col items-center gap-3 w-40">
              <motion.button
                key="m-fab-goal"
                initial={{ opacity: 0, y: 16, scale: 0.8 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 16, scale: 0.8 }}
                transition={{ duration: 0.15, delay: 0.05 }}
                onClick={() => { setFabOpen(false); navigate('/app/goals'); }}
                className="flex items-center gap-2 bg-ink border border-white/20 text-white px-4 py-3 rounded-full font-bold shadow-2xl text-sm whitespace-nowrap w-full justify-center pointer-events-auto"
              >
                <Flame size={16} className="text-mint" /> New Goal
              </motion.button>
              <motion.button
                key="m-fab-task"
                initial={{ opacity: 0, y: 16, scale: 0.8 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 16, scale: 0.8 }}
                transition={{ duration: 0.15 }}
                onClick={() => { setFabOpen(false); navigate('/app/tasks'); }}
                className="flex items-center gap-2 bg-ink border border-white/20 text-white px-4 py-3 rounded-full font-bold shadow-2xl text-sm whitespace-nowrap w-full justify-center pointer-events-auto"
              >
                <ListTodo size={16} className="text-sky-400" /> New Task
              </motion.button>
            </div>
          )}
        </AnimatePresence>

        <motion.button
          onClick={() => setFabOpen(!fabOpen)}
          whileTap={{ scale: 0.9 }}
          className="h-14 w-14 rounded-full bg-mint text-ink shadow-xl shadow-mint/30 grid place-items-center relative z-50 pointer-events-auto"
        >
          <motion.div animate={{ rotate: fabOpen ? 45 : 0 }} transition={{ duration: 0.2 }}>
            {fabOpen ? <X size={24} strokeWidth={3} /> : <Plus size={24} strokeWidth={3} />}
          </motion.div>
        </motion.button>
      </div>
'''

# We will inject new_mobile_fab right before the Desktop FAB
layout_content = layout_content.replace('{/* ─── Desktop FAB (bottom-right) ─── */}', new_mobile_fab + '\n      {/* ─── Desktop FAB (bottom-right) ─── */}')

with open(layout_path, 'w', encoding='utf-8') as f:
    f.write(layout_content)
print("Updated Layout.tsx")
