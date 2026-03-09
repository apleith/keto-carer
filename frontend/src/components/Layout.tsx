import { Outlet, NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  UtensilsCrossed,
  ShoppingCart,
  TrendingUp,
  Pill,
  Droplets,
  Settings,
} from "lucide-react";
import { cn } from "@/lib/utils";

const nav = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/meals", label: "Meal Planning", icon: UtensilsCrossed },
  { to: "/grocery", label: "Grocery List", icon: ShoppingCart },
  { to: "/progress", label: "Progress", icon: TrendingUp },
  { to: "/medications", label: "Medications", icon: Pill },
  { to: "/water", label: "Water", icon: Droplets },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Layout() {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 shrink-0 flex flex-col border-r border-[--color-border] bg-[--color-surface] p-4 gap-1">
        <div className="mb-6 px-2">
          <h1 className="text-lg font-semibold text-[--color-text] tracking-tight">
            🥑 keto-carer
          </h1>
        </div>
        {nav.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-[--color-accent] text-[--color-accent-foreground]"
                  : "text-[--color-text-muted] hover:text-[--color-text] hover:bg-[--color-border]"
              )
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto p-6 bg-[--color-background]">
        <Outlet />
      </main>
    </div>
  );
}
