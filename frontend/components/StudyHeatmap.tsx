/**
 * Study Heatmap — GitHub-style activity visualization
 * Arată activitatea de studiu din ultimele 12 săptămâni
 */
import { useMemo } from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { DUO } from '@/constants/duo';

interface StudyHeatmapProps {
  /** Map of 'YYYY-MM-DD' → number of exercises solved */
  activity: Record<string, number>;
  /** Number of weeks to show (default 12) */
  weeks?: number;
}

const DAY_LABELS = ['L', '', 'M', '', 'V', '', 'D'];
const MONTH_LABELS = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function getColor(count: number): string {
  if (count === 0) return DUO.surface;
  if (count <= 2) return '#1a4731';
  if (count <= 5) return '#166534';
  if (count <= 10) return '#22c55e';
  return DUO.green;
}

export default function StudyHeatmap({ activity, weeks = 12 }: StudyHeatmapProps) {
  const { grid, months, totalExercises, currentStreak, longestStreak } = useMemo(() => {
    const today = new Date();
    const totalDays = weeks * 7;
    const startDate = new Date(today);
    startDate.setDate(startDate.getDate() - totalDays + 1);

    // Align to Monday
    const dayOfWeek = startDate.getDay();
    const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
    startDate.setDate(startDate.getDate() + mondayOffset);

    // Build grid (7 rows x N cols)
    const grid: { count: number }[][] = [];
    const monthLabels: { label: string; col: number }[] = [];
    let lastMonth = -1;

    const current = new Date(startDate);
    let col = 0;

    while (current <= today) {
      const weekCol: typeof grid[0] = [];

      for (let row = 0; row < 7; row++) {
        const dateStr = current.toISOString().split('T')[0];
        const count = current <= today ? (activity[dateStr] || 0) : -1; // -1 = future
        const month = current.getMonth();

        if (month !== lastMonth && current <= today) {
          monthLabels.push({ label: MONTH_LABELS[month], col });
          lastMonth = month;
        }

        weekCol.push({ count });
        current.setDate(current.getDate() + 1);
      }

      grid.push(weekCol);
      col++;
    }

    // Calculate streaks
    let currentStreak = 0;
    const d = new Date(today);
    // Today may still be pending — don't break the streak on it
    if (!(activity[d.toISOString().split('T')[0]] > 0)) d.setDate(d.getDate() - 1);
    while (currentStreak < 365 && activity[d.toISOString().split('T')[0]] > 0) {
      currentStreak++;
      d.setDate(d.getDate() - 1);
    }

    let longestStreak = 0;
    let run = 0;
    const e = new Date(today);
    for (let i = 0; i < 365; i++) {
      if ((activity[e.toISOString().split('T')[0]] || 0) > 0) {
        run++;
        longestStreak = Math.max(longestStreak, run);
      } else {
        run = 0;
      }
      e.setDate(e.getDate() - 1);
    }

    const totalExercises = Object.values(activity).reduce((s, v) => s + v, 0);

    return { grid, months: monthLabels, totalExercises, currentStreak, longestStreak };
  }, [activity, weeks]);

  const CELL_SIZE = 14;
  const CELL_GAP = 3;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Activitate de Studiu</Text>
        <Text style={styles.subtitle}>{totalExercises} exercitii in {weeks} saptamani</Text>
      </View>

      {/* Heatmap */}
      <View style={styles.heatmapContainer}>
        {/* Day labels */}
        <View style={styles.dayLabels}>
          {DAY_LABELS.map((label, i) => (
            <View key={i} style={{ height: CELL_SIZE + CELL_GAP, justifyContent: 'center' }}>
              <Text style={styles.dayLabel}>{label}</Text>
            </View>
          ))}
        </View>

        {/* Grid */}
        <View style={styles.gridContainer}>
          {/* Month labels */}
          <View style={[styles.monthRow, { height: 16 }]}>
            {months.map((m, i) => (
              <Text
                key={i}
                style={[styles.monthLabel, { left: m.col * (CELL_SIZE + CELL_GAP) }]}
              >
                {m.label}
              </Text>
            ))}
          </View>

          {/* Cells */}
          <View style={styles.grid}>
            {grid.map((week, colIdx) => (
              <View key={colIdx} style={styles.weekCol}>
                {week.map((day, rowIdx) => (
                  <View
                    key={`${colIdx}-${rowIdx}`}
                    style={[
                      styles.cell,
                      {
                        width: CELL_SIZE,
                        height: CELL_SIZE,
                        backgroundColor: day.count < 0 ? 'transparent' : getColor(day.count),
                        borderRadius: 3,
                      },
                    ]}
                  />
                ))}
              </View>
            ))}
          </View>
        </View>
      </View>

      {/* Legend */}
      <View style={styles.legendRow}>
        <Text style={styles.legendText}>Mai putin</Text>
        {[0, 1, 3, 6, 11].map((count) => (
          <View
            key={count}
            style={[styles.legendCell, { backgroundColor: getColor(count) }]}
          />
        ))}
        <Text style={styles.legendText}>Mai mult</Text>
      </View>

      {/* Stats */}
      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{currentStreak}</Text>
          <Text style={styles.statLabel}>Streak curent</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{longestStreak}</Text>
          <Text style={styles.statLabel}>Cel mai lung</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>
            {totalExercises > 0 ? Math.round(totalExercises / Math.max(Object.keys(activity).length, 1)) : 0}
          </Text>
          <Text style={styles.statLabel}>Media/zi</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: DUO.card,
    borderRadius: 18,
    padding: 16,
    borderWidth: 1,
    borderColor: DUO.surface,
    gap: 12,
  },
  header: { gap: 2 },
  title: { fontSize: 16, fontWeight: '800', color: DUO.textPrimary },
  subtitle: { fontSize: 12, fontWeight: '600', color: DUO.textMuted },

  heatmapContainer: { flexDirection: 'row', gap: 6 },
  dayLabels: { width: 16, paddingTop: 16 },
  dayLabel: { fontSize: 9, fontWeight: '700', color: DUO.textMuted },
  gridContainer: { flex: 1 },
  monthRow: { position: 'relative', marginBottom: 4 },
  monthLabel: { position: 'absolute', fontSize: 9, fontWeight: '700', color: DUO.textMuted },
  grid: { flexDirection: 'row', gap: 3 },
  weekCol: { gap: 3 },
  cell: {},

  legendRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 4 },
  legendText: { fontSize: 10, fontWeight: '600', color: DUO.textMuted },
  legendCell: { width: 12, height: 12, borderRadius: 2 },

  statsRow: { flexDirection: 'row', justifyContent: 'center', gap: 0 },
  statItem: { flex: 1, alignItems: 'center', gap: 2 },
  statValue: { fontSize: 20, fontWeight: '900', color: DUO.green },
  statLabel: { fontSize: 10, fontWeight: '700', color: DUO.textMuted, textTransform: 'uppercase', letterSpacing: 0.5 },
  statDivider: { width: 1, height: 32, backgroundColor: DUO.surface, alignSelf: 'center' },
});
