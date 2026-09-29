import { useEffect, useState } from 'react';
import { learningApi } from '../api/learningApi';
import { Link } from 'react-router-dom';
import { BookOpenIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

export default function Topics() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const data = await learningApi.getTopics();
        setTopics(data);
      } catch (err) {
        console.error("Error fetching topics", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopics();
  }, []);

  if (loading) {
    return <div className="animate-pulse flex space-x-4 p-6">
      <div className="flex-1 space-y-6 py-1">
        <div className="h-4 bg-gray-200 rounded w-1/4"></div>
        <div className="space-y-3">
          <div className="h-24 bg-gray-200 rounded"></div>
          <div className="h-24 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>;
  }

  return (
    <div className="pt-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Chủ đề học tập</h1>
      <p className="text-gray-600 mb-8">Khám phá các chủ đề từ cơ bản đến nâng cao về Cơ sở Dữ liệu</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {topics.map((topic, idx) => (
          <motion.div 
            key={topic.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all group overflow-hidden"
          >
            <div className="h-32 bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center relative">
              {/* Abstract pattern */}
              <div className="absolute inset-0 opacity-20 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4IiBoZWlnaHQ9IjgiPgo8cmVjdCB3aWR0aD0iOCIgaGVpZ2h0PSI4IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMSIvPgo8cGF0aCBkPSJNMCAwbDhfOHptOCAwTDBfOHoiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLW9wYWNpdHk9IjAuNCIvPgo8L3N2Zz4=')]"></div>
              <BookOpenIcon className="h-16 w-16 text-white opacity-90" />
            </div>
            
            <div className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                {topic.name}
              </h2>
              <p className="text-gray-600 mb-6 text-sm line-clamp-2 h-10">
                {topic.description || 'Không có mô tả'}
              </p>
              
              <Link 
                to={`/topics/${topic.id}`}
                className="block w-full text-center bg-primary-50 text-primary-700 py-2.5 rounded-lg font-semibold hover:bg-primary-100 transition-colors"
              >
                Vào học ngay
              </Link>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
