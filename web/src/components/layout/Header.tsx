interface HeaderProps {
  userName?: string;
}

const Header = ({ userName = '이지은 팀장' }: HeaderProps) => {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-slate-800 bg-slate-900/60 px-6 py-4 backdrop-blur">
      <div>
        <h2 className="text-lg font-semibold text-slate-100">사내 통합 업무 현황판</h2>
        <p className="text-sm text-slate-400 mt-1">오늘도 성공적인 협업을 위해 필요한 정보를 모아두었습니다.</p>
      </div>
      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 rounded-full bg-slate-800/70 px-4 py-2 text-sm text-slate-300">
          <span className="i-ic-baseline-search" aria-hidden></span>
          <input
            type="search"
            placeholder="프로젝트, 태스크, 담당자를 검색"
            className="bg-transparent outline-none placeholder:text-slate-500 w-56"
          />
        </div>
        <button className="relative rounded-full bg-slate-800/70 p-3 text-slate-300 hover:text-indigo-300">
          <span className="i-ic-round-notifications" aria-hidden></span>
          <span className="absolute -top-0.5 -right-0.5 inline-flex h-2.5 w-2.5 rounded-full bg-rose-500"></span>
        </button>
        <div className="flex items-center gap-3 rounded-full bg-slate-800/70 px-3 py-2">
          <div className="h-9 w-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500" />
          <div className="hidden text-sm text-slate-200 sm:block">
            <p className="font-medium">{userName}</p>
            <p className="text-xs text-slate-400">Strategy & PMO</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
