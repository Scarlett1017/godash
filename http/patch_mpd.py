import os

file_path = "mpdParsing.go"

if not os.path.exists(file_path):
    print(f"错误: 找不到 {file_path}，请确保在 ~/godash/http 目录下运行。")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print("正在对 mpdParsing.go 进行安全手术 (字符串替换模式)...")

# --- 修复 1: 处理 PT12S 秒数解析 Bug (针对 758-769 行) ---
old_atoi = """	if strings.Contains(streamDuration, "S") {

		// get the seconds and convert to int
		s := strings.Split(streamDuration, ".")
		i2, err := strconv.Atoi(s[0])
		if err != nil {
			fmt.Println("*** Problem with converting segment seconds to int ***")
		}
		if i2 > 0 {
			totalTimeinSeconds += i2
		}
	}"""

new_atoi = """	if strings.Contains(streamDuration, "S") {
		s1 := strings.Replace(streamDuration, "S", "", -1)
		s2 := strings.Split(s1, ".")[0]
		i2, err := strconv.Atoi(s2)
		if err != nil {
			fmt.Printf("Warning: Atoi failed for seconds: %s\\n", s2)
		}
		if i2 > 0 {
			totalTimeinSeconds += i2
		}
	}"""

# --- 修复 2: 防止 GetMPDheightIndex 返回 -1 (针对 858 行) ---
old_height = "	return maxHeightIndex - 1"
new_height = """	if maxHeightIndex <= 0 {
		return 0
	}
	return maxHeightIndex - 1"""

# --- 修复 3: 防止分片总数计算为 0 (针对 705 行) ---
old_seg_details = "	return streamDuration / segmentDurations[mpdListIndex], segmentDurations"
new_seg_details = """	numSegments := streamDuration / segmentDurations[mpdListIndex]
	if numSegments <= 0 {
		numSegments = 1
	}
	return numSegments, segmentDurations"""

# 执行替换
content = content.replace(old_atoi, new_atoi)
content = content.replace(old_height, new_height)
content = content.replace(old_seg_details, new_seg_details)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 补丁手术完成！")