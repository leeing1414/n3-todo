interface HeaderProps {
  userName: string;
  department: string;
  onLogout?: () => void;
}

const Header = ({ userName, department, onLogout }: HeaderProps) => {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-slate-800 bg-slate-900/60 px-6 py-4 backdrop-blur">
      <div>
        <h2 className="text-lg font-semibold text-slate-100">사내 통합 업무 현황판</h2>
        <p className="mt-1 text-sm text-slate-400">오늘 해야 할 일과 프로젝트 상태를 한눈에 확인하세요.</p>
      </div>
      <div className="flex items-center gap-4">
        <div className="hidden items-center gap-2 rounded-full bg-slate-800/70 px-4 py-2 text-sm text-slate-300 md:flex">
          <span className="i-ic-baseline-search" aria-hidden></span>
          <input
            type="search"
            placeholder="프로젝트, 태스크, 담당자를 검색"
            className="w-56 bg-transparent outline-none placeholder:text-slate-500"
          />
        </div>
        <button className="relative rounded-full bg-slate-800/70 p-3 text-slate-300 transition hover:text-indigo-300">
          <span className="i-ic-round-notifications" aria-hidden></span>
          <span className="absolute -top-0.5 -right-0.5 inline-flex h-2.5 w-2.5 rounded-full bg-rose-500"></span>
        </button>
        <div className="flex items-center gap-3 rounded-full bg-slate-800/70 px-3 py-2">
          <div className="h-9 w-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500" />
          <div className="hidden text-sm text-slate-200 sm:block">
            <p className="font-medium">{userName}</p>
            <p className="text-xs text-slate-400">{department}</p>
          </div>
        </div>
        {onLogout && (
          <button
            type="button"
            onClick={onLogout}
            className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:border-indigo-400 hover:text-indigo-300"
          >
            로그아웃
          </button>
        )}
      </div>
    </header>
  );
};

export default Header;