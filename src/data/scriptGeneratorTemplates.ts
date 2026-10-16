export interface PartitionOption {
  id: string;
  name: string;
  partition: string;
  fileName: string;
  desc: string;
  defaultChecked: boolean;
  category: 'kernel' | 'recovery' | 'system' | 'security' | 'user';
  specialFlag?: string;
}

export const FLASH_PARTITIONS_LIST: PartitionOption[] = [
  {
    id: "p-boot",
    name: "كيرنل الإقلاع (Boot Kernel)",
    partition: "boot",
    fileName: "boot.img",
    desc: "ضروري للإقلاع وحل مشاكل التوقف على الشعار والروت",
    defaultChecked: true,
    category: "kernel"
  },
  {
    id: "p-init-boot",
    name: "بوت أندرويد الحديث (Init Boot)",
    partition: "init_boot",
    fileName: "init_boot.img",
    desc: "خاص بأجهزة أندرويد 13 و 14 و 15 لتمرير الروت وتفادي التعليق",
    defaultChecked: false,
    category: "kernel"
  },
  {
    id: "p-vbmeta",
    name: "التحقق الأمني وتجاوز الحماية (VBMeta Disabled)",
    partition: "vbmeta",
    fileName: "vbmeta.img",
    desc: "إيقاف التحقق من توقيع النظام وتفادي Bootloop بعد التعديل",
    defaultChecked: true,
    specialFlag: "--disable-verity --disable-verification",
    category: "security"
  },
  {
    id: "p-recovery",
    name: "ريكفري النظام (Recovery Image)",
    partition: "recovery",
    fileName: "recovery.img",
    desc: "وضع الاسترداد وتثبيت ريكفري معدل TWRP أو OrangeFox",
    defaultChecked: true,
    category: "recovery"
  },
  {
    id: "p-dtbo",
    name: "تعريفات البوردة والشاشة (DTBO)",
    partition: "dtbo",
    fileName: "dtbo.img",
    desc: "إصلاح الشاشة السوداء ومشاكل اللمس بعد تفليش غير مطابق",
    defaultChecked: false,
    category: "kernel"
  },
  {
    id: "p-super",
    name: "النظام المجمع الكامل (Super Partition)",
    partition: "super",
    fileName: "super.img",
    desc: "يحوي ملفات System و Vendor و Product لأندرويد 10 فما فوق (كبير الحجم)",
    defaultChecked: false,
    category: "system"
  },
  {
    id: "p-userdata",
    name: "بيانات المستخدم ومسح الذاكرة (Userdata Wipe)",
    partition: "userdata",
    fileName: "userdata.img",
    desc: "تنبيه: سيؤدي إلى فورمات ومسح جميع صور وملفات العميل بالكامل",
    defaultChecked: false,
    category: "user"
  },
  {
    id: "p-metadata",
    name: "تنسيق التشفير والتهيئة (Metadata)",
    partition: "metadata",
    fileName: "metadata.img",
    desc: "تهيئة مساحة التشفير للأجهزة المقفلة بخطأ Decryption Error",
    defaultChecked: false,
    category: "system"
  }
];

export interface ScriptGenerationConfig {
  deviceBrand: string;
  selectedPartitions: string[];
  rebootAtEnd: boolean;
  wipeDataPrompt: boolean;
  fastbootdMode: boolean;
  scriptType: 'bat' | 'sh';
}

export function generateFlashScript(config: ScriptGenerationConfig): { script: string; filename: string } {
  const isBat = config.scriptType === 'bat';
  const lines: string[] = [];

  if (isBat) {
    lines.push('@echo off');
    lines.push('chcp 65001 >nul');
    lines.push('color 0b');
    lines.push('title HMAX UNLOCKER — Fastboot Auto Flasher Tool');
    lines.push('echo ========================================================');
    lines.push(`echo    HMAX AUTOMATED FASTBOOT FLASHER — [${config.deviceBrand.toUpperCase()}]`);
    lines.push('echo    Generated via HMAX UNLOCKER Professional Portal');
    lines.push('echo ========================================================');
    lines.push('echo.');
    lines.push('echo [*] جارٍ فحص اتصال الجهاز بوضع Fastboot...');
    lines.push('fastboot devices');
    lines.push('echo.');
    lines.push('echo [*] قراءة معلومات الهاتف والبوت لودر:');
    lines.push('fastboot getvar product');
    lines.push('fastboot getvar unlocked');
    lines.push('echo.');
    lines.push('pause');
    lines.push('echo.');

    if (config.fastbootdMode) {
      lines.push('echo [*] التحويل إلى وضع الفاست بوت المطور Fastbootd لتفليش البارتشنات الديناميكية...');
      lines.push('fastboot reboot fastboot');
      lines.push('timeout /t 5 >nul');
      lines.push('echo.');
    }

    config.selectedPartitions.forEach((pId) => {
      const part = FLASH_PARTITIONS_LIST.find((p) => p.id === pId);
      if (!part) return;

      lines.push(`echo [*] جارٍ تفليش بارتيشن ${part.partition} [${part.fileName}]...`);
      if (part.specialFlag) {
        lines.push(`fastboot flash ${part.specialFlag} ${part.partition} ${part.fileName}`);
      } else {
        lines.push(`fastboot flash ${part.partition} ${part.fileName}`);
      }
    });

    if (config.wipeDataPrompt) {
      lines.push('echo.');
      lines.push('echo [*] جارٍ مسح الذاكرة وعمل فورمات مصنع (Wipe Userdata)...');
      lines.push('fastboot -w');
    }

    if (config.rebootAtEnd) {
      lines.push('echo.');
      lines.push('echo [*] اكتمل التفليش بنجاح 100%! جارٍ إعادة تشغيل الهاتف...');
      lines.push('fastboot reboot');
    }

    lines.push('echo.');
    lines.push('echo ========================================================');
    lines.push('echo    انتهت العملية بنجاح! مع تحيات فريق هيثم ماكس');
    lines.push('echo ========================================================');
    lines.push('pause');
  } else {
    // Shell Script (.sh)
    lines.push('#!/bin/bash');
    lines.push('echo "=== HMAX UNLOCKER Linux/Mac Fastboot Flasher ==="');
    lines.push('fastboot devices');
    if (config.fastbootdMode) {
      lines.push('fastboot reboot fastboot');
      lines.push('sleep 5');
    }
    config.selectedPartitions.forEach((pId) => {
      const part = FLASH_PARTITIONS_LIST.find((p) => p.id === pId);
      if (!part) return;
      if (part.specialFlag) {
        lines.push(`fastboot flash ${part.specialFlag} ${part.partition} ${part.fileName}`);
      } else {
        lines.push(`fastboot flash ${part.partition} ${part.fileName}`);
      }
    });
    if (config.wipeDataPrompt) lines.push('fastboot -w');
    if (config.rebootAtEnd) lines.push('fastboot reboot');
    lines.push('echo "=== Flashing Complete! ==="');
  }

  const filename = `HMAX_Flash_${config.deviceBrand.replace(/[^a-zA-Z0-9]/g, '_')}_${Date.now()}.${config.scriptType}`;
  return { script: lines.join('\n'), filename };
}
