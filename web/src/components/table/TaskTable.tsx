import { useMemo } from 'react';
import { flexRender, getCoreRowModel, useReactTable, createColumnHelper } from '@tanstack/react-table';

import type { Task } from '@types/index';

interface TaskTableProps {
  tasks: Task[];
}

const columnHelper = createColumnHelper<Task>();

const TaskTable = ({ tasks }: TaskTableProps) => {
  const columns = useMemo(
    () => [
      columnHelper.accessor('title', {
        header: '업무명',
        cell: (info) => <span className="font-medium text-slate-100">{info.getValue()}</span>,
      }),
      columnHelper.accessor('status', {
        header: '상태',
        cell: (info) => <span className="rounded-full bg-slate-800/60 px-2 py-1 text-xs capitalize text-indigo-300">{info.getValue().replace('_', ' ')}</span>,
      }),
      columnHelper.accessor('priority', {
        header: '우선순위',
        cell: (info) => <span className="text-sm text-slate-300">{info.getValue()}</span>,
      }),
      columnHelper.accessor('progress', {
        header: '진척도',
        cell: (info) => (
          <div className="flex items-center gap-2">
            <div className="h-1.5 w-full rounded-full bg-slate-800">
              <div className="h-full rounded-full bg-indigo-500" style={{ width: `${info.getValue()}%` }} />
            </div>
            <span className="w-10 text-right text-xs text-slate-400">{info.getValue()}%</span>
          </div>
        ),
      }),
      columnHelper.accessor('due_date', {
        header: '마감일',
        cell: (info) => (
          <span className="text-sm text-slate-300">
            {info.getValue() ? new Date(info.getValue()!).toLocaleDateString() : '미정'}
          </span>
        ),
      }),
    ],
    []
  );

  const table = useReactTable({
    data: tasks,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">데이터 그리드</h4>
      <p className="text-sm text-slate-400">대량 데이터를 필터링하고 정렬하세요.</p>
      <div className="mt-4 overflow-hidden rounded-2xl border border-slate-800/60">
        <table className="w-full border-collapse text-sm text-slate-200">
          <thead className="bg-slate-900/70">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="px-4 py-3 text-left font-medium uppercase tracking-wide text-xs text-slate-400">
                    {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="border-t border-slate-800/60 hover:bg-slate-900/40">
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="px-4 py-3">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
            {!table.getRowModel().rows.length && (
              <tr>
                <td colSpan={columns.length} className="px-4 py-6 text-center text-slate-500">
                  표시할 업무 데이터가 없습니다.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default TaskTable;
