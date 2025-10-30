import { useEffect, useState } from 'react';
import { DragDropContext, Draggable, Droppable, DropResult } from '@hello-pangea/dnd';

import type { Task } from '@types/index';

const STATUS_LABELS: Record<string, string> = {
  todo: '대기 중',
  in_progress: '진행 중',
  review: '검토 필요',
  blocked: '이슈',
  done: '완료',
};

interface KanbanBoardProps {
  tasks: Task[];
}

const KanbanBoard = ({ tasks }: KanbanBoardProps) => {
  const [columns, setColumns] = useState<Record<string, Task[]>>({});

  useEffect(() => {
    const grouped = tasks.reduce<Record<string, Task[]>>((acc, task) => {
      acc[task.status] = acc[task.status] ? [...acc[task.status], task] : [task];
      return acc;
    }, {});
    setColumns(grouped);
  }, [tasks]);

  const onDragEnd = (result: DropResult) => {
    const { source, destination } = result;
    if (!destination) return;

    const sourceColumn = columns[source.droppableId] ?? [];
    const destinationColumn = columns[destination.droppableId] ?? [];

    const task = sourceColumn[source.index];
    if (!task) return;

    const updatedSource = [...sourceColumn];
    updatedSource.splice(source.index, 1);

    const updatedDestination = [...destinationColumn];
    updatedDestination.splice(destination.index, 0, task);

    setColumns({
      ...columns,
      [source.droppableId]: updatedSource,
      [destination.droppableId]: updatedDestination,
    });
  };

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <div className="flex items-center justify-between">
        <h4 className="text-lg font-semibold text-slate-100">칸반 보드</h4>
        <p className="text-sm text-slate-400">상태 기반 드래그앤드롭으로 업무 이동</p>
      </div>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          {Object.entries(STATUS_LABELS).map(([status, label]) => (
            <Droppable droppableId={status} key={status}>
              {(provided, snapshot) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  className={`flex min-h-[320px] flex-col rounded-2xl border border-slate-800/60 bg-slate-900/40 p-4 transition ${
                    snapshot.isDraggingOver ? 'border-indigo-500/60 bg-indigo-500/10' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <h5 className="text-sm font-semibold text-slate-200">{label}</h5>
                    <span className="rounded-full bg-slate-800 px-2 py-1 text-xs text-slate-400">
                      {(columns[status] ?? []).length}
                    </span>
                  </div>
                  <div className="mt-4 space-y-3">
                    {(columns[status] ?? []).map((task, index) => (
                      <Draggable draggableId={task.id} index={index} key={task.id}>
                        {(dragProvided, dragSnapshot) => (
                          <article
                            ref={dragProvided.innerRef}
                            {...dragProvided.draggableProps}
                            {...dragProvided.dragHandleProps}
                            className={`rounded-xl border border-slate-800/60 bg-slate-800/40 p-3 text-sm text-slate-200 shadow-lg shadow-slate-900/20 transition ${
                              dragSnapshot.isDragging ? 'border-indigo-400/70 bg-slate-900/80' : ''
                            }`}
                          >
                            <p className="font-medium line-clamp-2">{task.title}</p>
                            <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
                              <span>우선순위: {task.priority}</span>
                              {task.due_date && <span>마감: {new Date(task.due_date).toLocaleDateString()}</span>}
                            </div>
                          </article>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>
    </section>
  );
};

export default KanbanBoard;
