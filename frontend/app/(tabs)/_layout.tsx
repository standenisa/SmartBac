import { Tabs } from 'expo-router';
import React from 'react';
import { Platform, View, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface TabIconProps {
  emoji: string;
  label: string;
  focused: boolean;
  colors: [string, string];
}

const TabIcon = ({ emoji, label, focused, colors }: TabIconProps) => (
  <View style={styles.tabIconContainer}>
    {focused ? (
      <LinearGradient
        colors={colors}
        style={styles.activeTab}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.tabEmoji}>{emoji}</Text>
      </LinearGradient>
    ) : (
      <View style={styles.inactiveTab}>
        <Text style={styles.tabEmoji}>{emoji}</Text>
      </View>
    )}
    <Text style={[styles.tabLabel, focused && styles.tabLabelActive]}>
      {label}
    </Text>
  </View>
);

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#8b5cf6',
        tabBarInactiveTintColor: '#9ca3af',
        headerShown: false,
        tabBarStyle: {
          backgroundColor: 'white',
          borderTopWidth: 0,
          height: Platform.OS === 'ios' ? 88 : 70,
          paddingTop: 8,
          paddingBottom: Platform.OS === 'ios' ? 28 : 10,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: -4 },
          shadowOpacity: 0.08,
          shadowRadius: 12,
          elevation: 10,
        },
        tabBarShowLabel: false,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Acasa',
          tabBarIcon: ({ focused }) => (
            <TabIcon
              emoji="🏠"
              label="Acasa"
              focused={focused}
              colors={['#a78bfa', '#8b5cf6']}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="exercises"
        options={{
          title: 'Exercitii',
          tabBarIcon: ({ focused }) => (
            <TabIcon
              emoji="✏️"
              label="Exercitii"
              focused={focused}
              colors={['#f87171', '#ef4444']}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="flashcards"
        options={{
          title: 'Flashcards',
          tabBarIcon: ({ focused }) => (
            <TabIcon
              emoji="🃏"
              label="Cards"
              focused={focused}
              colors={['#a78bfa', '#8b5cf6']}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="streaks"
        options={{
          title: 'Streaks',
          tabBarIcon: ({ focused }) => (
            <TabIcon
              emoji="🔥"
              label="Streaks"
              focused={focused}
              colors={['#fb923c', '#f97316']}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: 'Chat AI',
          tabBarIcon: ({ focused }) => (
            <TabIcon
              emoji="💬"
              label="Chat"
              focused={focused}
              colors={['#34d399', '#10b981']}
            />
          ),
        }}
      />
      {/* Hidden screens - accessible from other places */}
      <Tabs.Screen
        name="exam"
        options={{
          href: null,
        }}
      />
      <Tabs.Screen
        name="theory"
        options={{
          href: null,
        }}
      />
      <Tabs.Screen
        name="pomodoro"
        options={{
          href: null,
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          href: null,
        }}
      />
      <Tabs.Screen
        name="progress"
        options={{
          href: null,
        }}
      />
      <Tabs.Screen
        name="achievements"
        options={{
          href: null,
        }}
      />
      <Tabs.Screen
        name="analytics"
        options={{
          href: null,
        }}
      />
    </Tabs>
  );
}

const styles = StyleSheet.create({
  tabIconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
  },
  activeTab: {
    width: 44,
    height: 44,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#8b5cf6',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  inactiveTab: {
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  tabEmoji: {
    fontSize: 20,
  },
  tabLabel: {
    fontSize: 10,
    fontWeight: '600',
    color: '#9ca3af',
  },
  tabLabelActive: {
    color: '#8b5cf6',
  },
});
