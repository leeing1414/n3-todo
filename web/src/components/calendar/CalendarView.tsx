import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';

import type { Task } from '@types/index';

interface CalendarViewProps {
  tasks: Task[];
}

const CalendarView = ({ tasks }: CalendarViewProps) => {
  const events = tasks
    .filter((task) => task.due_date)
    .map((task) => ({
      id: task.id,
      title: task.title,
      start: task.start_date ?? task.due_date,
      end: task.due_date,
      backgroundColor: task.status === 'done' ? '#22c55e' : '#6366f1',
      borderColor: 'transparent',
      display: 'block',
    }));

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">캘린더 뷰</h4>
      <p className="text-sm text-slate-400">마감 일정과 주요 이벤트</p>
      <div className="mt-4 overflow-hidden rounded-2xl border border-slate-800/60 bg-slate-900/50 p-2">
        <FullCalendar
          height="100%"
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView="dayGridMonth"
          events={events}
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay',
          }}
          locale="ko"
        />
      </div>
    </section>
  );
};

export default CalendarView;
