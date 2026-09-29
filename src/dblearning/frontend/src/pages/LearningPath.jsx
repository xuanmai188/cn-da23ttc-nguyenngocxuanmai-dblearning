import { useEffect, useState } from 'react';
import { recommendationApi } from '../api/recommendationApi';
import { MapIcon, CheckCircleIcon, SparklesIcon, ArrowRightIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function LearningPath() {
  const [recommendations, setRecommendations] = useState([]);
  const [profile, setProfile] = useState(null);
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
        console.error("Error", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Đang tạo lộ trình cá nhân hóa...</div>;

  return (
    <div className="max-w-5xl mx-auto pt-8 pb-20 space-y-8">
      <div className="bg-gradient-to-br from-indigo-600 to-purple-700 rounded-2xl p-8 text-white shadow-xl relative overflow-hidden">
        <div className="relative z-10">
          <h1 className="text-3xl font-bold mb-4 flex items-center">
            <MapIcon className="h-8 w-8 mr-3 text-indigo-200" />
            Lộ Trình Học Tập Của Bạn
          </h1>
          <p className="text-indigo-100 max-w-2xl text-lg leading-relaxed">
            {profile?.total_items_completed === 0 ? 'Dựa vào kết quả khảo sát đầu vào, AI của chúng tôi đã xây dựng lộ trình khởi đầu dành riêng cho bạn.' : 'Dựa vào lịch sử học tập và kết quả bài kiểm tra, AI của chúng tôi đã cập nhật lộ trình tiếp theo dành riêng cho bạn.'}
          </p>
          
          <div className="mt-6 flex items-center space-x-6">
            <div className="bg-white/10 px-4 py-2 rounded-lg backdrop-blur-sm border border-white/20">
              <span className="block text-indigo-200 text-sm">Chủ đề thế mạnh</span>
              <span className="font-bold text-xl uppercase">{profile?.preferred_difficulty || 'Chưa rõ'}</span>
            </div>
            <div className="bg-white/10 px-4 py-2 rounded-lg backdrop-blur-sm border border-white/20">
              <span className="block text-indigo-200 text-sm">Điểm TB Quiz</span>
              <span className="font-bold text-xl">{profile?.avg_quiz_score ? profile.avg_quiz_score.toFixed(1) : 0}%</span>
            </div>
          </div>
        </div>
        <SparklesIcon className="absolute -bottom-4 -right-4 h-48 w-48 text-white/5" />
      </div>

      <div className="relative">
        <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-200"></div>
        
        <div className="space-y-8">
          {recommendations.length > 0 ? (
            recommendations.map((rec, index) => (
              <motion.div 
                key={rec.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="relative pl-24 pr-4"
              >
                <div className="absolute left-6 top-1/2 -mt-4 h-8 w-8 rounded-full bg-white border-4 border-indigo-500 flex items-center justify-center shadow-md">
                  <div className="h-2 w-2 bg-indigo-500 rounded-full"></div>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow relative overflow-hidden group">
                  <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
                  
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full uppercase tracking-wider">
                          Bước {index + 1}
                        </span>
                        <span className="text-gray-400 text-sm font-medium">
                          Mức độ phù hợp: {(rec.score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-indigo-600 transition-colors">
                        {rec.item?.title}
                      </h3>
                      <p className="text-gray-500 mb-4">{rec.item?.description}</p>
                    </div>
                    <span className="text-sm font-medium px-3 py-1 bg-gray-50 text-gray-600 rounded-lg whitespace-nowrap">
                      ~{rec.item?.estimated_minutes} phút
                    </span>
                  </div>

                  <Link 
                    to={/learning/ + rec.item?.id}
                    className="inline-flex items-center px-4 py-2 bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 font-medium transition-colors"
                  >
                    Bắt đầu học ngay
                    <ArrowRightIcon className="ml-2 h-4 w-4" />
                  </Link>
                </div>
              </motion.div>
            ))
          ) : (
            <div className="pl-24">
              <div className="bg-gray-50 rounded-xl p-8 text-center border border-dashed border-gray-300">
                <p className="text-gray-500">Bạn chưa có dữ liệu học tập đủ nhiều để AI gợi ý. Hãy hoàn thành thêm bài học hoặc bài kiểm tra nhé!</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
