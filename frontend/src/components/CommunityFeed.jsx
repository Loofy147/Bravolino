import React from 'react';

const dummyAchievements = [
  { id: 1, user: 'Ahmed', achievement: 'Completed the "Arabic Letters" lesson' },
  { id: 2, user: 'Fatima', achievement: 'Reached Level 5 in Math' },
  { id: 3, user: 'Youssef', achievement: 'Earned the "Science Explorer" badge' },
  { id: 4, user: 'Aisha', achievement: 'Completed the "Water Cycle" lesson' },
];

const CommunityFeed = () => {
  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Community Feed</h2>
      <div className="space-y-4">
        {dummyAchievements.map((item) => (
          <div key={item.id} className="bg-white p-4 rounded-lg shadow">
            <p>
              <span className="font-bold">{item.user}</span> {item.achievement}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommunityFeed;
