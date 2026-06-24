import React, { createContext, useContext, useEffect, useState } from 'react';

export type Mode = '25/5' | '50/10' | 'custom';

export interface PomodoroState {
  timeLeft: number;
  isRunning: boolean;
  mode: Mode;
  isBreak: boolean;
  workMinutes: number;
  breakMinutes: number;
  showLogForm: boolean;
  setShowLogForm: (v: boolean) => void;
  startTimer: () => void;
  pauseTimer: () => void;
  resetTimer: () => void;
  setMode: (m: Mode) => void;
  setCustom: (w: number, b: number) => void;
}

const PomodoroContext = createContext<PomodoroState | null>(null);

export function PomodoroProvider({ children }: { children: React.ReactNode }) {
  const [mode, setModeState] = useState<Mode>('25/5');
  const [workMinutes, setWorkMinutes] = useState(25);
  const [breakMinutes, setBreakMinutes] = useState(5);
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [isBreak, setIsBreak] = useState(false);
  const [showLogForm, setShowLogForm] = useState(false);

  useEffect(() => {
    let interval: any;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => setTimeLeft(t => t - 1), 1000);
    } else if (isRunning && timeLeft === 0) {
      if (!isBreak) {
        setIsBreak(true);
        setTimeLeft(breakMinutes * 60);
        if ('speechSynthesis' in window) {
          const u = new SpeechSynthesisUtterance(`Focus session complete. Take a break for ${breakMinutes} minutes.`);
          window.speechSynthesis.speak(u);
        }
      } else {
        setIsRunning(false);
        setIsBreak(false);
        setTimeLeft(workMinutes * 60);
        setShowLogForm(true);
        if ('speechSynthesis' in window) {
          const u = new SpeechSynthesisUtterance(`Break completed. Time to focus.`);
          window.speechSynthesis.speak(u);
        }
      }
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft, isBreak, workMinutes, breakMinutes]);

  function setMode(m: Mode) {
    setModeState(m);
    setIsRunning(false);
    setIsBreak(false);
    if (m === '25/5') { setWorkMinutes(25); setBreakMinutes(5); setTimeLeft(25 * 60); }
    if (m === '50/10') { setWorkMinutes(50); setBreakMinutes(10); setTimeLeft(50 * 60); }
  }

  function setCustom(w: number, b: number) {
    setModeState('custom');
    setWorkMinutes(w);
    setBreakMinutes(b);
    setIsRunning(false);
    setIsBreak(false);
    setTimeLeft(w * 60);
  }

  function startTimer() { setIsRunning(true); }
  function pauseTimer() { setIsRunning(false); }
  function resetTimer() {
    setIsRunning(false);
    setIsBreak(false);
    setTimeLeft(workMinutes * 60);
    setShowLogForm(false);
  }

  return (
    <PomodoroContext.Provider value={{ timeLeft, isRunning, mode, isBreak, workMinutes, breakMinutes, showLogForm, setShowLogForm, startTimer, pauseTimer, resetTimer, setMode, setCustom }}>
      {children}
    </PomodoroContext.Provider>
  );
}

export function usePomodoro() {
  const ctx = useContext(PomodoroContext);
  if (!ctx) throw new Error("usePomodoro must be used within PomodoroProvider");
  return ctx;
}
