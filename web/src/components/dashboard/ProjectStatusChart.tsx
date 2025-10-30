import { Pie, PieChart, ResponsiveContainer, Cell, Legend, Tooltip } from 'recharts';

interface ProjectStatusChartProps {
  data: Array<Record<string, unknown>>;
}

const COLORS = ['#38bdf8', '#a855f7', '#f97316', '#22c55e', '#f87171'];

const ProjectStatusChart = ({ data }: ProjectStatusChartProps) => {
  const chartData = data.map((item, index) => ({
    name: String(item.status ?? `상태 ${index + 1}`),
    value: Number(item.count ?? 0),
  }));

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">프로젝트 상태 분포</h4>
      <p className="text-sm text-slate-400">상태별 프로젝트 비중</p>
      <div className="mt-4 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={chartData} innerRadius={60} outerRadius={90} paddingAngle={3} dataKey="value">
              {chartData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: 12 }}
              formatter={(value: number) => `${value.toLocaleString()}건`}
            />
            <Legend verticalAlign="bottom" height={36} wrapperStyle={{ color: '#cbd5f5' }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
};

export default ProjectStatusChart;
