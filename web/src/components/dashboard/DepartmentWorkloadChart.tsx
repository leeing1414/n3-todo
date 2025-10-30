import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface DepartmentWorkloadChartProps {
  data: Array<Record<string, unknown>>;
}

const DepartmentWorkloadChart = ({ data }: DepartmentWorkloadChartProps) => {
  const chartData = data.map((item, index) => ({
    name: String(item.department_id ?? `조직 ${index + 1}`),
    value: Number(item.count ?? 0),
  }));

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">부서별 프로젝트 부담</h4>
      <p className="text-sm text-slate-400">진행 중인 프로젝트 수 기준</p>
      <div className="mt-4 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="name" stroke="#94a3b8" tickLine={false} axisLine={false} />
            <YAxis stroke="#94a3b8" tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: 12 }}
              formatter={(value: number) => `${value.toLocaleString()}건`}
            />
            <Bar dataKey="value" fill="url(#workloadGradient)" radius={[12, 12, 12, 12]} />
            <defs>
              <linearGradient id="workloadGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.9} />
                <stop offset="100%" stopColor="#6366f1" stopOpacity={0.7} />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
};

export default DepartmentWorkloadChart;
