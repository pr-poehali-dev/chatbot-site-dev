import Icon from '@/components/ui/icon';

const AnimatedIcons = () => {
  const topIcons = [
    { name: 'Table', delay: '0s', x: '5%', y: '10%', size: 32 },
    { name: 'BarChart3', delay: '0.5s', x: '15%', y: '20%', size: 28 },
    { name: 'Bot', delay: '1s', x: '25%', y: '5%', size: 36 },
    { name: 'Settings', delay: '1.5s', x: '35%', y: '15%', size: 30 },
    { name: 'TrendingUp', delay: '2s', x: '45%', y: '8%', size: 34 },
    { name: 'Zap', delay: '2.5s', x: '55%', y: '18%', size: 28 },
    { name: 'MessageSquare', delay: '3s', x: '65%', y: '12%', size: 32 },
    { name: 'Workflow', delay: '3.5s', x: '75%', y: '6%', size: 30 },
    { name: 'Sparkles', delay: '4s', x: '85%', y: '16%', size: 34 },
    { name: 'Database', delay: '4.5s', x: '95%', y: '10%', size: 28 },
  ];

  const bottomIcons = [
    { name: 'Cpu', delay: '0.3s', x: '8%', y: '85%', size: 30 },
    { name: 'Globe', delay: '0.8s', x: '18%', y: '90%', size: 32 },
    { name: 'Lightbulb', delay: '1.3s', x: '28%', y: '88%', size: 28 },
    { name: 'Rocket', delay: '1.8s', x: '38%', y: '92%', size: 34 },
    { name: 'Target', delay: '2.3s', x: '48%', y: '86%', size: 30 },
    { name: 'Code', delay: '2.8s', x: '58%', y: '91%', size: 32 },
    { name: 'Activity', delay: '3.3s', x: '68%', y: '87%', size: 28 },
    { name: 'Users', delay: '3.8s', x: '78%', y: '93%', size: 30 },
    { name: 'Shield', delay: '4.3s', x: '88%', y: '89%', size: 32 },
  ];

  return (
    <>
      <div className="fixed top-0 left-0 w-full h-screen overflow-hidden pointer-events-none opacity-15 z-0">
        {topIcons.map((icon, i) => (
          <div
            key={`top-${i}`}
            className="absolute animate-float"
            style={{
              left: icon.x,
              top: icon.y,
              animationDelay: icon.delay,
              animationDuration: '6s'
            }}
          >
            <Icon name={icon.name as any} size={icon.size} className="text-cyan-400" />
          </div>
        ))}
        {bottomIcons.map((icon, i) => (
          <div
            key={`bottom-${i}`}
            className="absolute animate-float"
            style={{
              left: icon.x,
              top: icon.y,
              animationDelay: icon.delay,
              animationDuration: '7s'
            }}
          >
            <Icon name={icon.name as any} size={icon.size} className="text-cyan-400" />
          </div>
        ))}
      </div>
    </>
  );
};

export default AnimatedIcons;