/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: Introduction to Physical AI and ROS2 Framework',
      items: [
        'ch1-introduction/sub1-what-is-physical-ai',
        'ch1-introduction/sub2-ros2-overview',
        'ch1-introduction/sub3-setup-env',
        'ch1-introduction/sub4-architecture-elements',
        'ch1-introduction/sub5-packages-workspaces',
        'ch1-introduction/sub6-commands-tools'
      ],
    },
    {
      type: 'category',
      label: 'Modules',
      items: [
        'modules/mod1-ros2-deep-dive'
      ],
    },
    {
      type: 'category',
      label: 'Labs',
      items: [
        'labs/lab1-1-ros2-installation',
        'labs/lab1-2-first-nodes'
      ],
    },
  ],
};

module.exports = sidebars;