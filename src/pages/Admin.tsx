import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Icon from '@/components/ui/icon';

interface Lead {
  id: number;
  name: string;
  telegram: string;
  niche: string;
  created_at: string;
}

const Admin = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://functions.poehali.dev/c7d5b56c-1086-40c8-b213-728b53170def');
      const data = await response.json();
      setLeads(data.leads || []);
    } catch (error) {
      console.error('Failed to fetch leads:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-background text-foreground p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2">Админ-панель</h1>
            <p className="text-muted-foreground">Список всех заявок</p>
          </div>
          <Button onClick={fetchLeads} className="bg-cyan-500 hover:bg-cyan-600">
            <Icon name="RefreshCw" size={18} className="mr-2" />
            Обновить
          </Button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="flex gap-2">
              <div className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse" />
              <div className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
              <div className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="glass p-4 rounded-lg flex items-center justify-between">
              <p className="text-lg">Всего заявок: <span className="font-bold text-cyan-400">{leads.length}</span></p>
            </div>

            <div className="grid gap-4">
              {leads.map((lead) => (
                <Card key={lead.id} className="glass p-6 border-border/50 hover:border-cyan-500/30 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 space-y-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-cyan-500/20 flex items-center justify-center">
                          <Icon name="User" size={20} className="text-cyan-400" />
                        </div>
                        <div>
                          <h3 className="text-xl font-semibold">{lead.name}</h3>
                          <p className="text-sm text-muted-foreground">ID: #{lead.id}</p>
                        </div>
                      </div>
                      
                      <div className="grid md:grid-cols-2 gap-4 pl-13">
                        <div className="flex items-center gap-2">
                          <Icon name="Send" size={16} className="text-cyan-400" />
                          <span className="text-sm">{lead.telegram}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Icon name="Briefcase" size={16} className="text-cyan-400" />
                          <span className="text-sm">{lead.niche}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Icon name="Clock" size={14} />
                        <span>{formatDate(lead.created_at)}</span>
                      </div>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="mt-4"
                        onClick={() => window.open(`https://t.me/${lead.telegram.replace('@', '')}`, '_blank')}
                      >
                        <Icon name="MessageCircle" size={14} className="mr-2" />
                        Написать
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {leads.length === 0 && (
              <div className="text-center py-12">
                <Icon name="Inbox" size={48} className="mx-auto text-muted-foreground mb-4" />
                <p className="text-muted-foreground">Пока нет заявок</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Admin;