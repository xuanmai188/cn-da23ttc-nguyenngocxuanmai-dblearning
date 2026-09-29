import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { recommendationApi } from '../api/recommendationApi';
import OnboardingModal from '../components/OnboardingModal';
import { Link } from 'react-router-dom';
import { FireIcon, ChartBarIcon, StarIcon, ArrowRightIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profData, recData] = await Promise.all([
          recommendationApi.getProfile(),
          recommendationApi.getRecommendations()
        ]);
        setProfile(profData);
        setRecommendations(recData.recommendations || []);
      } catch (err) {
        console.error("Error fetching dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);


  const handleOnboardingComplete = () => {
    // Reload profile and recommendations
    setLoading(true);
    Promise.all([
      recommendationApi.getProfile(),
      recommendationApi.getRecommendations()
    ]).then(([profData, recData]) => {
      setProfile(profData);
      setRecommendations(recData.recommendations || []);
    }).finally(() => setLoading(false));
  };

  if (loading) {

    return <div className="animate-pulse space-y-6 pt-6">
      <div className="h-32 bg-gray-200 rounded-xl"></div>
      <div className="h-64 bg-gray-200 rounded-xl"></div>
    </div>;
  }


  return (
    <div className="space-y-6 pt-6">
      {profile && profile.is_onboarded === false && profile.total_items_completed === 0 && (
        <OnboardingModal onComplete={handleOnboardingComplete} />
      )}

      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 text-white shadow-lg">
        <h1 className="text-3xl font-bold mb-2">Chào mừng trở lại, {user?.full_name}! 👋</h1>
        <p className="text-primary-100 mb-6 max-w-2xl">Tiếp tục hành trình chinh phục Cơ sở Dữ liệu. Hôm nay bạn muốn học gì?</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white/10 rounded-xl p-4 flex items-center backdrop-blur-sm">
            <div className="p-3 bg-white/20 rounded-lg mr-4">
              <StarIcon className="h-6 w-6 text-yellow-300" />
            </div>
            <div>
              <p className="text-primary-100 text-sm">Điểm trung bình</p>
              <p className="text-2xl font-bold">{profile?.avg_quiz_score ? Math.round(profile.avg_quiz_score) : 0}</p>
            </div>
          </div>
          <div className="bg-white/10 rounded-xl p-4 flex items-center backdrop-blur-sm">
            <div className="p-3 bg-white/20 rounded-lg mr-4">
              <ChartBarIcon className="h-6 w-6 text-green-300" />
            </div>
            <div>
              <p className="text-primary-100 text-sm">Bài đã học</p>
              <p className="text-2xl font-bold">{profile?.total_items_completed || 0}</p>
            </div>
          </div>
          <div className="bg-white/10 rounded-xl p-4 flex items-center backdrop-blur-sm">
            <div className="p-3 bg-white/20 rounded-lg mr-4">
              <FireIcon className="h-6 w-6 text-red-300" />
            </div>
            <div>
              <p className="text-primary-100 text-sm">Chuỗi học tập</p>
              <p className="text-2xl font-bold">{profile?.learning_streak ?? 0} ngày</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <SparklesIcon className="h-6 w-6 text-primary-500 mr-2" />
          AI Gợi ý cho bạn
        </h2>
        
        {recommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((rec, idx) => (
              <motion.div 
                key={rec.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
              >
                <div className="h-2 bg-primary-500"></div>
                <div className="p-5">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-semibold px-2 py-1 bg-secondary-100 text-secondary-700 rounded-full">
                      {rec.item?.content_type === 'document' ? 'Tài liệu' : rec.item?.content_type === 'quiz' ? 'Bài tập' : 'Flashcard'}
                    </span>
                    <span className="text-xs text-gray-500 font-medium">~{rec.item?.estimated_minutes} phút</span>
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2 line-clamp-2">{rec.item?.title}</h3>
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">{rec.item?.description}</p>
                  <Link 
                    to={rec.item?.content_type === "quiz" ? `/quiz/${rec.item?.id}` : rec.item?.content_type === "flashcard_set" ? `/flashcard/${rec.item?.id}` : `/learning/${rec.item?.id}`}
                    className="inline-flex items-center text-sm font-semibold text-primary-600 hover:text-primary-700"
                  >
                    Bắt đầu học
                    <ArrowRightIcon className="h-4 w-4 ml-1" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-xl p-8 text-center border border-gray-100 shadow-sm">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-50 mb-4">
              <BookOpenIcon className="h-8 w-8 text-primary-500" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Bắt đầu khóa học</h3>
            <p className="text-gray-500 mb-6">Bạn chưa có gợi ý nào. Hãy bắt đầu học chủ đề đầu tiên để AI có thể phân tích và gợi ý cho bạn nhé.</p>
            <Link to="/topics" className="bg-primary-600 text-white px-6 py-2.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors">
              Xem danh sách chủ đề
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

// Helper icons
function SparklesIcon(props) {
  return (
    <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09l2.846.813-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  );
}
function BookOpenIcon(props) {
  return (
    <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
    </svg>
  );
}
