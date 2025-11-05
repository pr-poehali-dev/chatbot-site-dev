import Icon from '@/components/ui/icon';

const AnimatedIcons = () => {
  const icons = [
    { name: 'Table', delay: '0s', x: '10%' },
    { name: 'BarChart3', delay: '0.5s', x: '30%' },
    { name: 'Bot', delay: '1s', x: '50%' },
    { name: 'Settings', delay: '1.5s', x: '70%' },
    { name: 'TrendingUp', delay: '2s', x: '90%' },
  ];

  return (
    <div className="absolute top-0 left-0 w-full h-32 overflow-hidden pointer-events-none opacity-20">
      {icons.map((icon, i) => (
        <div
          key={i}
          className="absolute animate-float"
          style={{
            left: icon.x,
            animationDelay: icon.delay,
            animationDuration: '4s'
          }}
        >
          <Icon name={icon.name as any} size={32} className="text-cyan-400" />
        </div>
      ))}
    </div>
  );
};

export default AnimatedIcons;
