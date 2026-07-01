import { Tabs } from 'expo-router';
import React from 'react';
import { Platform, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { DUO } from '@/constants/duo';

interface TabIconProps {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  focused: boolean;
  activeColor: string;
}

const TabIcon = ({ icon, label, focused, activeColor }: TabIconProps) => (
  <View style={styles.tabIconContainer}>
    <View style={[
      styles.tabCircle,
      focused && {
        backgroundColor: activeColor + '20',
        borderBottomColor: activeColor + '40',
        shadowColor: activeColor,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.5,
        shadowRadius: 12,
        elevation: 4,
      },
    ]}>
      <Ionicons
        name={icon}
        size={22}
        color={focused ? activeColor : DUO.textMuted}
      />
    </View>
    <Text style={[styles.tabLabel, focused && { color: activeColor }]}>{label}</Text>
  </View>
);

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: DUO.card,
          borderTopWidth: 1,
          borderTopColor: DUO.surface,
          height: Platform.OS === 'ios' ? 88 : 70,
          paddingTop: 8,
          paddingBottom: Platform.OS === 'ios' ? 28 : 10,
        },
        tabBarShowLabel: false,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Acasa',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="home" label="Acasa" focused={focused} activeColor={DUO.green} />
          ),
        }}
      />
      <Tabs.Screen
        name="exercises"
        options={{
          title: 'Exercitii',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="create" label="Exercitii" focused={focused} activeColor={DUO.blue} />
          ),
        }}
      />
      <Tabs.Screen
        name="flashcards"
        options={{
          title: 'Cards',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="albums" label="Cards" focused={focused} activeColor={DUO.purple} />
          ),
        }}
      />
      <Tabs.Screen
        name="streaks"
        options={{
          title: 'Streaks',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="flame" label="Streaks" focused={focused} activeColor={DUO.orange} />
          ),
        }}
      />
      <Tabs.Screen
        name="scanner"
        options={{
          title: 'Scanner',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="scan" label="Scanner" focused={focused} activeColor={DUO.cyan} />
          ),
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: 'Chat',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="chatbubbles" label="Chat" focused={focused} activeColor={DUO.green} />
          ),
        }}
      />
      <Tabs.Screen
        name="study-plan"
        options={{
          title: 'Plan AI',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="compass" label="Plan AI" focused={focused} activeColor={DUO.purple} />
          ),
        }}
      />
      <Tabs.Screen
        name="analytics"
        options={{
          title: 'Predictie',
          tabBarIcon: ({ focused }) => (
            <TabIcon icon="stats-chart" label="Predictie" focused={focused} activeColor={DUO.yellow} />
          ),
        }}
      />
      <Tabs.Screen name="exam" options={{ href: null }} />
      <Tabs.Screen name="theory" options={{ href: null }} />
      <Tabs.Screen name="pomodoro" options={{ href: null }} />
      <Tabs.Screen name="progress" options={{ href: null }} />
      <Tabs.Screen name="achievements" options={{ href: null }} />
      <Tabs.Screen name="leagues" options={{ href: null }} />
      <Tabs.Screen name="quick-practice" options={{ href: null }} />
    </Tabs>
  );
}

const styles = StyleSheet.create({
  tabIconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    gap: 3,
  },
  tabCircle: {
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: DUO.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomWidth: 3,
    borderBottomColor: DUO.cardDark,
  },
  tabLabel: {
    fontSize: 10,
    fontWeight: '700',
    color: DUO.textMuted,
  },
});
