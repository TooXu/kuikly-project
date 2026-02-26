package com.tooxu.kuiklyproject.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Apple Intelligence 风格的聊天页面
 * 特性：
 * 1. IM 聊天框布局
 * 2. 点击按钮触发屏幕四周彩色光晕效果（便于调试）
 * 3. 光晕具有呼吸动画效果
 */
@Composable
fun AppleIntelligenceChatPage() {
    // 控制光晕效果的状态
    var isGlowing by remember { mutableStateOf(false) }
    
    // 呼吸动画的无限循环
    val infiniteTransition = rememberInfiniteTransition()
    val breatheAlpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 0.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 2000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        )
    )
    
    // 彩色光晕的颜色渐变
    val glowColors = listOf(
        Color(0xFF667EEA), // 蓝紫色
        Color(0xFF8E44AD), // 紫色
        Color(0xFFE74C3C), // 红色
        Color(0xFFF39C12), // 橙色
        Color(0xFF2ECC71), // 绿色
        Color(0xFF3498DB)  // 蓝色
    )
    
    val currentGlowColor by animateColorAsState(
        targetValue = if (isGlowing) {
            // 随机选择一个颜色进行渐变
            val randomIndex = (System.currentTimeMillis() / 3000).toInt() % glowColors.size
            glowColors[randomIndex]
        } else {
            Color.Transparent
        },
        animationSpec = tween(durationMillis = 1000)
    )
    
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
            .then(
                if (isGlowing) {
                    Modifier.border(
                        width = 8.dp,
                        brush = Brush.radialGradient(
                            colors = listOf(currentGlowColor.copy(alpha = breatheAlpha), Color.Transparent),
                            center = Alignment.Center,
                            radius = 2000f
                        )
                    )
                } else {
                    Modifier
                }
            )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // 聊天消息区域
            ChatMessagesArea()
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // 底部输入和按钮区域
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // 输入框（简化版）
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height(48.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .background(Color.DarkGray.copy(alpha = 0.5f))
                        .border(
                            width = 1.dp,
                            color = Color.White.copy(alpha = 0.3f),
                            shape = RoundedCornerShape(24.dp)
                        )
                ) {
                    Text(
                        text = "Message...",
                        color = Color.White.copy(alpha = 0.7f),
                        modifier = Modifier
                            .align(Alignment.CenterStart)
                            .padding(start = 16.dp)
                    )
                }
                
                Spacer(modifier = Modifier.width(8.dp))
                
                // Apple Intelligence 按钮 - 点击触发，便于调试
                Button(
                    onClick = { isGlowing = !isGlowing },
                    modifier = Modifier
                        .size(56.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color.White,
                        contentColor = Color.Black
                    ),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Text(
                        text = "AI",
                        fontWeight = FontWeight.Bold,
                        fontSize = 16.sp
                    )
                }
            }
        }
    }
}

@Composable
private fun ChatMessagesArea() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .weight(1f)
    ) {
        // 示例消息 - 用户消息
        MessageBubble(
            message = "Hello! How can I help you today?",
            isUser = false,
            timestamp = "10:30 AM"
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        // 示例消息 - AI 消息
        MessageBubble(
            message = "I'm working on something amazing with Compose!",
            isUser = true,
            timestamp = "10:31 AM"
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        // 示例消息 - AI 消息
        MessageBubble(
            message = "The Apple Intelligence effect looks stunning!",
            isUser = false,
            timestamp = "10:32 AM"
        )
    }
}

@Composable
private fun MessageBubble(
    message: String,
    isUser: Boolean,
    timestamp: String
) {
    val backgroundColor = if (isUser) Color.Blue else Color.Gray.copy(alpha = 0.3f)
    
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Box(
            modifier = Modifier
                .width(IntrinsicSize.Min)
                .padding(horizontal = 8.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(backgroundColor)
                .padding(12.dp)
        ) {
            Column {
                Text(
                    text = message,
                    color = Color.White,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = timestamp,
                    color = Color.White.copy(alpha = 0.7f),
                    fontSize = 10.sp
                )
            }
        }
    }
}