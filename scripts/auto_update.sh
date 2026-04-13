#!/bin/bash
# Java 面试题每日自动更新脚本
# 搜索最新面经 → 去重 → 整理答案 → 更新文档 → 群通知

PROJECT_DIR="/root/projects/java-interview-by-company"
LOG_DIR="/root/.openclaw/workspace-dev/logs"
LOG_FILE="$LOG_DIR/java-interview-update.log"
NOTICE_FILE="$LOG_DIR/java-interview-notice.md"

# 大厂列表
COMPANIES=("阿里巴巴" "腾讯" "字节跳动" "美团" "京东" "华为" "百度" "快手" "小红书" "滴滴" "网易" "拼多多")

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 使用 agent-reach 搜索最新社招面经
search_interviews() {
  local company="$1"
  local date=$(date '+%Y-%m')
  
  # 使用 DuckDuckGo 搜索社招面经
  local query="${company} Java 社招面经 ${date} 真题 后端"
  
  log "搜索: $query"
  
  # 实际的深度整理由 OpenClaw Agent 完成
  # 此脚本主要用于文件操作和推送
}

# 推送到远程仓库（双仓库推送）
push_to_remote() {
  cd "$PROJECT_DIR"
  
  # 配置 Git
  git config user.email "dev-agent@openclaw"
  git config user.name "dev-agent"
  
  # 检查是否有变更
  if git diff --quiet && git diff --staged --quiet; then
    log "无变更需要推送"
    return 0
  fi
  
  # 提交变更
  git add -A
  git commit -m "[Auto] 更新社招面经 $(date '+%Y-%m-%d')"
  
  # 推送到 Gitee (origin)
  git push origin main
  log "已推送至 Gitee 远程仓库"
  
  # 推送到 GitHub (github)
  git push github main
  log "已推送至 GitHub 远程仓库"
}

# 去重检查
check_duplicate() {
  local question="$1"
  local doc_file="$2"
  
  # 转小写去空格
  local normalized=$(echo "$question" | tr '[:upper:]' '[:lower:]' | tr -s ' ')
  
  # 检查文档中是否已存在
  if grep -qi "$normalized" "$doc_file" 2>/dev/null; then
    return 0  # 重复
  fi
  return 1  # 不重复
}

# 主流程
main() {
  log "=== 开始每日面经更新 ==="
  
  total_new=0
  updates=""
  
  for company in "${COMPANIES[@]}"; do
    log "处理: $company"
    
    # 搜索
    results=$(search_interviews "$company")
    
    if [ -n "$results" ]; then
      new_count=$(echo "$results" | wc -l)
      log "找到 $new_count 条结果"
      
      # 这里需要进一步处理：去重、整理答案
      # 实际的深度整理由 OpenClaw Agent 完成
      
      updates="$updates\n- $company: $new_count 条"
      total_new=$((total_new + new_count))
    else
      log "无新结果"
    fi
  done
  
  # 生成通知
  if [ $total_new -gt 0 ]; then
    cat > "$NOTICE_FILE" << EOF
# Java 面经更新通知

**更新时间:** $(date '+%Y-%m-%d %H:%M:%S')

**新增面经:** $total_new 条

## 各厂更新情况
$updates

**详细内容:** 请查看项目文档

EOF
    log "通知文件已生成"
    echo "updated"
  else
    log "今日无新增"
    echo "no_update"
  fi
  
  log "=== 更新完成 ==="
}

main