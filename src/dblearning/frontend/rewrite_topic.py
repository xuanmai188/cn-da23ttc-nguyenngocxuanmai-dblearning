import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/TopicDetail.jsx"
content = """import { useEffect, useState } from 'react';
import { learningApi } from '../api/learningApi';
import { useParams, Link } from 'react-router-dom';
import { DocumentTextIcon, QuestionMarkCircleIcon, RectangleStackIcon, PlayCircleIcon } from '@heroicons/react/24/outline';
import { CheckCircleIcon } from '@heroicons/react/24/solid';

export default function TopicDetail() {
  const { topicId } = useParams();
  const [topic, setTopic] = useState(null);
  const [completedItems, setCompletedItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopic = async () => {
      try {
        const data = await learningApi.getTopicDetails(topicId);
        setTopic(data);
        try {
          const comp = await learningApi.getCompletedItems();
          setCompletedItems(comp || []);
        } catch (e) {
          console.error(e);
        }
      } catch (err) {
        console.error("Error fetching topic detail", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopic();
  }, [topicId]);

  if (loading) return <div className="p-8 text-center text-gray-500">Đang tải...</div>;
  if (!topic) return <div className="p-8 text-center text-red-500">Không tìm thấy chủ đề</div>;

  const getItemIcon = (type) => {
    if (type === 'document') return <DocumentTextIcon className="h-6 w-6 text-blue-500" />;
    if (type === 'quiz') return <QuestionMarkCircleIcon className="h-6 w-6 text-red-500" />;
    if (type === 'flashcard_set') return <RectangleStackIcon className="h-6 w-6 text-orange-500" />;
    return <PlayCircleIcon className="h-6 w-6 text-gray-500" />;
  };

  const getUrl = (item) => {
    if (item.content_type === 'quiz') return `/quiz/${item.id}`;
    if (item.content_type === 'flashcard_set') return `/flashcard/${item.id}`;
    return `/learning/${item.id}`;
  };

  return (
    <div className="pt-6 max-w-4xl mx-auto">
      <Link to="/topics" className="text-primary-600 hover:underline mb-4 inline-block">&larr; Quay lại danh sách</Link>
      
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{topic.name}</h1>
        <p className="text-gray-600 text-lg">{topic.description}</p>
      </div>

      <h2 className="text-xl font-bold text-gray-800 mb-6">Lộ trình bài học ({topic.items?.length || 0} bài)</h2>
      
      <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-200 before:to-transparent">
        {topic.items?.map((item, idx) => (
          <div key={item.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
            {/* Timeline Icon */}
            <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-gray-100 text-gray-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
              {getItemIcon(item.content_type)}
            </div>
            
            {/* Card */}
            <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs font-semibold px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
                  {item.difficulty?.toUpperCase()}
                </span>
                <span className="text-xs text-gray-400 font-medium">~{item.estimated_minutes}p</span>
              </div>
              <h3 className="font-bold text-gray-900 text-lg mb-1 flex items-center">
                {item.title}
                {completedItems.includes(item.id) && <CheckCircleIcon className="h-5 w-5 text-green-500 ml-2" title="Đã hoàn thành" />}
              </h3>
              <p className="text-sm text-gray-500 mb-4 line-clamp-2">{item.description}</p>
              
              <Link 
                to={getUrl(item)}
                className="inline-flex items-center text-sm font-semibold text-primary-600 hover:text-primary-700"
              >
                Học ngay &rarr;
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("TopicDetail.jsx rewritten")
