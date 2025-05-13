import { Children, StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import {
  BrowserRouter,
  RouterProvider,
  createBrowserRouter,
} from "react-router-dom";
import Homepage from "./routes/homePage/Homepage.jsx";
import SignInPage from "./routes/signInPage/SignInPage.jsx";
import RootLayout from "./layouts/rootLayout/RootLayout.jsx";
import SignUpPage from "./routes/signUpPage/SignUppage.jsx";
import DashboardLayout from "./layouts/dashboardLayout/DashboardLayout.jsx";

import ChatPage from "./routes/chatPage/ChatPage.jsx";
import DashboardPage from "./routes/dashboardPage/DashBoardPage.jsx";

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      {
        path: "/",
        element: <Homepage />,
      },
      {
        path: "/sign-in/*",
        element: <SignInPage />,
      },
      {
        path: "/sign-up/*",
        element: <SignUpPage />,
      },
      {
        element: <DashboardLayout />,
        children: [
          {
            path: "/dashboard",
            element: <DashboardPage />,
          },
          {
            path: "/dashboard/chat/:id",
            element: <ChatPage />,
          },
        ],
      },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  
    <RouterProvider router={router} />
  
);
