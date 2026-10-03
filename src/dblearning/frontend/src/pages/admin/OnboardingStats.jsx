import React, { useState, useEffect } from 'react';
import { adminApi } from '../../api/adminApi';
import OverviewTab from '../../components/admin/survey/OverviewTab';
import QuestionsTab from '../../components/admin/survey/QuestionsTab';
import ResultsTab from '../../components/admin/survey/ResultsTab';
import PreviewModal from '../../components/admin/survey/PreviewModal';
import { PlayIcon } from '@heroicons/react/24/outline';

export default function OnboardingStats() {
  const [activeTab, setActiveTab] = useState('overview');
  const [survey, setSurvey] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [topics, setTopics] = useState([]);
  const [results, setResults] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [surveysData, statsData, topicsData, resultsData] = await Promise.all([
        adminApi.getSurveys(),
        adminApi.getSurveyStats(),
        adminApi.getTopics(),
        adminApi.getSurveyResults()
      ]);
      
      const activeSurvey = surveysData.find(s => s.is_active) || surveysData[0];
      setSurvey(activeSurvey);
      setStats(statsData);
      setTopics(topicsData);
      setResults(resultsData || []);
      
      if (activeSurvey) {
        const qData = await adminApi.getSurveyQuestions(activeSurvey.id);
        setQuestions(qData);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <div className="text-center py-10">Đang tải dữ liệu...</div>;

  return (
    <div className="pb-10">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Khảo sát đầu vào</h1>
          <p className="text-slate-500 mt-1">Quản lý bộ khảo sát giúp xác định kiến thức, nhu cầu và mục tiêu học tập ban đầu của sinh viên.</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={() => setIsPreviewOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-50 text-indigo-700 font-medium rounded-lg hover:bg-indigo-100 transition-colors border border-indigo-100"
          >
            <PlayIcon className="w-5 h-5" />
            <span>Xem trước khảo sát</span>
          </button>
        </div>
      </div>

      <div className="flex gap-6 border-b border-slate-200 mb-6">
        <button 
          onClick={() => setActiveTab('overview')} 
          className={`pb-3 px-2 font-medium border-b-2 transition-colors ${activeTab === 'overview' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          1. Tổng quan
        </button>
        <button 
          onClick={() => setActiveTab('questions')} 
          className={`pb-3 px-2 font-medium border-b-2 transition-colors ${activeTab === 'questions' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          2. Quản lý câu hỏi
        </button>
        <button 
          onClick={() => setActiveTab('results')} 
          className={`pb-3 px-2 font-medium border-b-2 transition-colors ${activeTab === 'results' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          3. Kết quả khảo sát
        </button>
      </div>

      <div className="animate-in fade-in duration-200">
        {activeTab === 'overview' && (
          <OverviewTab 
            survey={survey} 
            questions={questions} 
            stats={stats} 
            totalStudents={stats.total_users || 0}
            onToggleStatus={async () => {
              if(!survey) return;
              try {
                if(survey.is_active) {
                  // toggle off is tricky if it's the only one, assume deactivate endpoint exists or we use PUT
                  await adminApi.updateSurvey(survey.id, { is_active: false });
                } else {
                  await adminApi.activateSurvey(survey.id);
                }
                fetchData();
              } catch(e) { console.error(e); alert("Lỗi khi thay đổi trạng thái"); }
            }}
          />
        )}
        
        {activeTab === 'questions' && (
          <QuestionsTab 
            survey={survey} 
            questions={questions} 
            topics={topics} 
            refreshData={fetchData} 
          />
        )}
        
        {activeTab === 'results' && (
          <ResultsTab 
            results={results} 
            stats={stats} 
            totalStudents={stats.total_users || 0} 
          />
        )}
      </div>

      {isPreviewOpen && (
        <PreviewModal 
          survey={survey} 
          questions={questions} 
          onClose={() => setIsPreviewOpen(false)} 
        />
      )}
    </div>
  );
}
