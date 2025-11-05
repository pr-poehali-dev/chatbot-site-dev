import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import Icon from '@/components/ui/icon';
import { useToast } from '@/hooks/use-toast';
import AnimatedIcons from '@/components/AnimatedIcons';
import ChatBot from '@/components/ChatBot';

const Index = () => {
  const { toast } = useToast();
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isChatMinimized, setIsChatMinimized] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    telegram: '',
    niche: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "Заявка отправлена!",
      description: "Скоро свяжусь с вами в Telegram",
    });
    setFormData({ name: '', telegram: '', niche: '' });
  };

  const services = [
    { icon: 'Bot', title: 'Telegram-боты', desc: 'Под любой сценарий и задачу' },
    { icon: 'Sparkles', title: 'AI-агенты', desc: 'Автоворонки с искусственным интеллектом' },
    { icon: 'Workflow', title: 'Интеграции', desc: 'CRM, GetCourse, любые сервисы' },
    { icon: 'Lightbulb', title: 'Консультации', desc: 'Помогу выстроить автоматизацию' }
  ];

  const segments = [
    { icon: 'GraduationCap', title: 'Эксперты', desc: 'Автоматизация продаж и обучения' },
    { icon: 'Scissors', title: 'Салоны и услуги', desc: 'Запись без менеджера' },
    { icon: 'Rocket', title: 'Стартапы', desc: 'AI внутри продукта' },
    { icon: 'Megaphone', title: 'Агентства', desc: 'White-label и подряд' }
  ];

  const steps = [
    { num: '01', title: 'Заявка', desc: 'Оставляете заявку или проходите квиз' },
    { num: '02', title: 'Сценарий', desc: 'Получаете готовый план работы' },
    { num: '03', title: 'Настройка', desc: 'Запуск и интеграция системы' },
    { num: '04', title: 'Работа', desc: 'Бот работает — вы отдыхаете' }
  ];

  const cases = [
    { 
      title: 'Бот для онлайн-школы',
      niche: 'Образование',
      desc: 'Автоматическая запись на курсы, оплата, выдача доступов',
      result: '+40% заявок'
    },
    {
      title: 'AI-консультант для e-commerce',
      niche: 'Интернет-магазин',
      desc: 'Подбор товаров, ответы на вопросы, обработка заказов',
      result: '70% запросов без человека'
    },
    {
      title: 'Запись в салон красоты',
      niche: 'Услуги',
      desc: 'Выбор мастера, времени, напоминания, отзывы',
      result: '0 пропущенных клиентов'
    }
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <AnimatedIcons />
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-500/10 via-background to-background pointer-events-none" />
      
      <div className="relative z-10">
        <section className="min-h-screen flex items-center justify-center px-4 py-20">
          <div className="max-w-4xl mx-auto text-center space-y-8 animate-fade-in">
            <div className="inline-flex items-center gap-2 glass px-4 py-2 rounded-full text-sm text-cyan-400">
              <Icon name="Sparkles" size={16} />
              <span>Telegram • AI • Автоматизация</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold leading-tight">
              Чат-боты и AI-системы,
              <br />
              <span className="neon-glow text-cyan-400">которые работают вместо вас</span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Автоматизирую продажи, консультации и поддержку через Telegram-ботов и AI-агентов. Под ключ и без головной боли.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="neon-border bg-cyan-500 hover:bg-cyan-600 text-background text-lg px-8"
                onClick={() => {
                  setIsChatOpen(true);
                  setIsChatMinimized(false);
                }}
              >
                <Icon name="MessageSquare" size={20} className="mr-2" />
                Поговорить с AI-консультантом
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="glass glass-hover text-lg px-8"
                onClick={() => window.open('https://t.me/yourusername', '_blank')}
              >
                <Icon name="Send" size={20} className="mr-2" />
                Написать в Telegram
              </Button>
            </div>
          </div>
        </section>

        <section className="px-4 py-20">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16 space-y-4">
              <h2 className="text-4xl md:text-5xl font-bold">Что я делаю</h2>
              <p className="text-muted-foreground text-lg">Решаю задачи бизнеса через технологии</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {services.map((service, i) => (
                <Card key={i} className="glass glass-hover p-6 space-y-4 border-border/50">
                  <div className="w-12 h-12 rounded-xl bg-cyan-500/10 flex items-center justify-center">
                    <Icon name={service.icon as any} size={24} className="text-cyan-400" />
                  </div>
                  <h3 className="text-xl font-semibold">{service.title}</h3>
                  <p className="text-muted-foreground">{service.desc}</p>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="px-4 py-20 bg-gradient-to-b from-transparent via-cyan-500/5 to-transparent">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16 space-y-4">
              <h2 className="text-4xl md:text-5xl font-bold">Для кого это</h2>
              <p className="text-muted-foreground text-lg">Решения под вашу нишу</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {segments.map((segment, i) => (
                <Card key={i} className="glass glass-hover p-6 space-y-3 text-center border-border/50">
                  <div className="text-4xl mb-2">
                    <Icon name={segment.icon as any} size={40} className="mx-auto text-cyan-400" />
                  </div>
                  <h3 className="text-lg font-semibold">{segment.title}</h3>
                  <p className="text-sm text-muted-foreground">{segment.desc}</p>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="px-4 py-20">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16 space-y-4">
              <h2 className="text-4xl md:text-5xl font-bold">Как работает</h2>
              <p className="text-muted-foreground text-lg">Простой процесс от идеи до запуска</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {steps.map((step, i) => (
                <div key={i} className="space-y-4">
                  <div className="text-6xl font-bold text-cyan-400/20">{step.num}</div>
                  <h3 className="text-xl font-semibold">{step.title}</h3>
                  <p className="text-muted-foreground">{step.desc}</p>
                  {i < steps.length - 1 && (
                    <Icon name="ArrowRight" size={24} className="text-cyan-400/40 hidden lg:block absolute right-0 top-8" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="px-4 py-20 bg-gradient-to-b from-transparent via-cyan-500/5 to-transparent">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16 space-y-4">
              <h2 className="text-4xl md:text-5xl font-bold">Примеры работ</h2>
              <p className="text-muted-foreground text-lg">Реальные кейсы и результаты</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cases.map((caseItem, i) => (
                <Card key={i} className="glass glass-hover p-6 space-y-4 border-border/50">
                  <div className="inline-block px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 text-sm">
                    {caseItem.niche}
                  </div>
                  <h3 className="text-xl font-semibold">{caseItem.title}</h3>
                  <p className="text-muted-foreground text-sm">{caseItem.desc}</p>
                  <div className="pt-4 border-t border-border/50">
                    <p className="text-cyan-400 font-semibold">{caseItem.result}</p>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="px-4 py-20">
          <div className="max-w-2xl mx-auto">
            <Card className="glass p-8 md:p-12 space-y-8 neon-border border-cyan-500/20">
              <div className="text-center space-y-4">
                <h2 className="text-3xl md:text-4xl font-bold">Готовы начать?</h2>
                <p className="text-muted-foreground">Оставьте заявку и получите готовый план автоматизации</p>
              </div>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Ваше имя</label>
                  <Input
                    placeholder="Александр"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="glass border-border/50"
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Telegram</label>
                  <Input
                    placeholder="@username"
                    value={formData.telegram}
                    onChange={(e) => setFormData({ ...formData, telegram: e.target.value })}
                    className="glass border-border/50"
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Ниша / Задача</label>
                  <Textarea
                    placeholder="Онлайн-школа, нужна автоматизация записи на курсы"
                    value={formData.niche}
                    onChange={(e) => setFormData({ ...formData, niche: e.target.value })}
                    className="glass border-border/50 min-h-24"
                    required
                  />
                </div>
                
                <Button type="submit" size="lg" className="w-full neon-border bg-cyan-500 hover:bg-cyan-600 text-background">
                  <Icon name="Send" size={20} className="mr-2" />
                  Отправить заявку
                </Button>
              </form>
              
              <div className="text-center pt-6 border-t border-border/50">
                <p className="text-sm text-muted-foreground mb-4">Или напишите напрямую</p>
                <Button variant="outline" className="glass glass-hover">
                  <Icon name="MessageCircle" size={20} className="mr-2" />
                  Написать в Telegram
                </Button>
              </div>
            </Card>
          </div>
        </section>

        <footer className="px-4 py-12 border-t border-border/50">
          <div className="max-w-6xl mx-auto text-center space-y-4">
            <p className="text-muted-foreground">
              © 2024 AI-автоматизация. Делаю боты, которые работают.
            </p>
            <div className="flex justify-center gap-6">
              <a href="#" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                <Icon name="Send" size={24} />
              </a>
              <a href="#" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                <Icon name="Mail" size={24} />
              </a>
            </div>
          </div>
        </footer>
      </div>
      {isChatOpen && (
        <ChatBot 
          onClose={() => setIsChatOpen(false)} 
          isMinimized={isChatMinimized}
          onToggleMinimize={() => setIsChatMinimized(!isChatMinimized)}
        />
      )}
    </div>
  );
};

export default Index;