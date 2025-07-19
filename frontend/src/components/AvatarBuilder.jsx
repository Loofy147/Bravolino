import React, { useState } from 'react';

const AvatarBuilder = () => {
  const [avatar, setAvatar] = useState({
    skinColor: '#F2D0B7',
    hairColor: '#3A2A2A',
    eyeColor: '#6B4226',
    clothing: 't-shirt',
    accessory: 'none',
  });

  const handleColorChange = (e) => {
    const { name, value } = e.target;
    setAvatar((prevAvatar) => ({ ...prevAvatar, [name]: value }));
  };

  const handleSelectChange = (e) => {
    const { name, value } = e.target;
    setAvatar((prevAvatar) => ({ ...prevAvatar, [name]: value }));
  };

  return (
    <div className="flex flex-col items-center p-4">
      <h2 className="text-2xl font-bold mb-4">Create Your Avatar</h2>
      <div className="w-48 h-48 bg-gray-300 rounded-full mb-4" style={{ backgroundColor: avatar.skinColor }}>
        {/* Simplified avatar representation */}
        <div className="w-full h-1/4" style={{ backgroundColor: avatar.hairColor }}></div>
        <div className="flex justify-around items-center h-1/4">
          <div className="w-4 h-4 rounded-full" style={{ backgroundColor: avatar.eyeColor }}></div>
          <div className="w-4 h-4 rounded-full" style={{ backgroundColor: avatar.eyeColor }}></div>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="skinColor" className="block text-sm font-medium text-gray-700">
            Skin Color
          </label>
          <input
            type="color"
            id="skinColor"
            name="skinColor"
            value={avatar.skinColor}
            onChange={handleColorChange}
            className="mt-1 block w-full"
          />
        </div>
        <div>
          <label htmlFor="hairColor" className="block text-sm font-medium text-gray-700">
            Hair Color
          </label>
          <input
            type="color"
            id="hairColor"
            name="hairColor"
            value={avatar.hairColor}
            onChange={handleColorChange}
            className="mt-1 block w-full"
          />
        </div>
        <div>
          <label htmlFor="eyeColor" className="block text-sm font-medium text-gray-700">
            Eye Color
          </label>
          <input
            type="color"
            id="eyeColor"
            name="eyeColor"
            value={avatar.eyeColor}
            onChange={handleColorChange}
            className="mt-1 block w-full"
          />
        </div>
        <div>
          <label htmlFor="clothing" className="block text-sm font-medium text-gray-700">
            Clothing
          </label>
          <select
            id="clothing"
            name="clothing"
            value={avatar.clothing}
            onChange={handleSelectChange}
            className="mt-1 block w-full"
          >
            <option value="t-shirt">T-shirt</option>
            <option value="sweater">Sweater</option>
            <option value="dress">Dress</option>
          </select>
        </div>
        <div>
          <label htmlFor="accessory" className="block text-sm font-medium text-gray-700">
            Accessory
          </label>
          <select
            id="accessory"
            name="accessory"
            value={avatar.accessory}
            onChange={handleSelectChange}
            className="mt-1 block w-full"
          >
            <option value="none">None</option>
            <option value="glasses">Glasses</option>
            <option value="hat">Hat</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default AvatarBuilder;
