import React from 'react';
import CommunityFeed from './CommunityFeed';
import UserProgress from './UserProgress';

const ParentDashboard = () => {
  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Parent Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="text-xl font-bold mb-2">Your Child's Progress</h3>
          <div className="space-y-4">
            <UserProgress subject="Arabic" progress={75} />
            <UserProgress subject="Math" progress={50} />
            <UserProgress subject="Science" progress={90} />
          </div>
        </div>
        <div>
          <CommunityFeed />
        </div>
      </div>
    </div>
  );
};

export default ParentDashboard;
