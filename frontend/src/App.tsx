import React from "react";
import ReactDOM from "react-dom/client";
import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom";
import "./styles/global.css";
import { Layout } from "./components/Layout";
import { PomodoroProvider } from "./context/PomodoroContext";
import { Achievements, Analytics, Calendar, Dashboard, Goals, Journal, Landing, Login, Notifications, Pomodoro, ResetPassword, Settings, Tasks, VerifyEmail, Guide } from "./pages/Pages";

const router = createBrowserRouter([
  { path: "/", element: <Landing /> },
  { path: "/login", element: <Login /> },
  { path: "/reset-password", element: <ResetPassword /> },
  { path: "/verify-email", element: <VerifyEmail /> },
  {
    path: "/app",
    element: <Layout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "goals", element: <Goals /> },
      { path: "tasks", element: <Tasks /> },
      { path: "analytics", element: <Analytics /> },
      { path: "calendar", element: <Calendar /> },
      { path: "journal", element: <Journal /> },
      { path: "pomodoro", element: <Pomodoro /> },
      { path: "achievements", element: <Achievements /> },
      { path: "notifications", element: <Notifications /> },
      { path: "guide", element: <Guide /> },
      { path: "settings", element: <Settings /> }
    ]
  },
  { path: "*", element: <Navigate to="/" /> }
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <PomodoroProvider>
      <RouterProvider router={router} />
    </PomodoroProvider>
  </React.StrictMode>
);
