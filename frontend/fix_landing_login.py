import re

pages_path = 'src/pages/Pages.tsx'
with open(pages_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Landing Page Mobile Header
old_header = '''      <header className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mx-auto max-w-7xl flex items-center justify-between glass px-6 py-3 rounded-2xl border border-white/10 shadow-2xl backdrop-blur-xl"
        >
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-mint text-ink font-black text-lg shadow-[0_0_15px_rgba(94,243,179,0.5)]">M</div>
            <span className="text-xl font-bold tracking-tight">Momentum</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/login" className="text-sm font-bold text-white/70 hover:text-white transition-colors">Login</Link>
            <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'register')} className="text-sm font-bold bg-white text-ink px-5 py-2 rounded-lg hover:bg-white/90 transition-all hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.2)]">Register</Link>
          </div>
        </motion.div>
      </header>'''

new_header = '''      <header className="fixed top-0 left-0 right-0 z-50 px-3 sm:px-6 py-4">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mx-auto max-w-7xl flex items-center justify-between glass px-4 sm:px-6 py-3 rounded-2xl border border-white/10 shadow-2xl backdrop-blur-xl"
        >
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="grid h-8 w-8 sm:h-10 sm:w-10 place-items-center rounded-xl bg-mint text-ink font-black text-base sm:text-lg shadow-[0_0_15px_rgba(94,243,179,0.5)] shrink-0">M</div>
            <span className="text-lg sm:text-xl font-bold tracking-tight hidden sm:block">Momentum</span>
          </div>
          <div className="flex items-center gap-3 sm:gap-4">
            <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'login')} className="text-sm font-bold text-white/70 hover:text-white transition-colors">Login</Link>
            <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'register')} className="text-sm font-bold bg-white text-ink px-4 sm:px-5 py-2 rounded-lg hover:bg-white/90 transition-all hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.2)]">Register</Link>
          </div>
        </motion.div>
      </header>'''

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Replaced Landing header")
else:
    print("Could not find Landing header block")

# 2. Add Back to Home link in Login Component
old_login_main = '''    return (
      <main className="grid min-h-screen place-items-center bg-ink px-4 text-white">
        <form onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6">'''

new_login_main = '''    return (
      <main className="grid min-h-screen place-items-center bg-ink px-4 text-white relative">
        <div className="absolute top-6 left-6">
          <Link to="/" className="flex items-center gap-2 text-white/50 hover:text-white transition-colors font-bold text-sm">
            <ArrowRight size={16} className="rotate-180" /> Back to Home
          </Link>
        </div>
        <form onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6">'''

if old_login_main in content:
    content = content.replace(old_login_main, new_login_main)
    print("Replaced Login main")
else:
    print("Could not find Login main block")

with open(pages_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
