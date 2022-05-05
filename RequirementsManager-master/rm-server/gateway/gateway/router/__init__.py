from gateway.router.usermanager.login import login
from gateway.router.usermanager.register import register
from gateway.router.usermanager.user.create import user_create
from gateway.router.usermanager.user.delete import user_delete
from gateway.router.usermanager.user.edit import user_edit
from gateway.router.usermanager.user.profile import user_profile
from gateway.router.usermanager.user.list import user_list
from gateway.router.usermanager.user.list_all import user_list_all

from gateway.router.projectmanager.project.create import project_create
from gateway.router.projectmanager.project.delete import project_delete
from gateway.router.projectmanager.project.edit import project_edit
from gateway.router.projectmanager.project.list import project_list
from gateway.router.projectmanager.project.profile import project_profile
from gateway.router.projectmanager.project.user.list import project_user_list
from gateway.router.projectmanager.project.user.edit import project_user_edit
from gateway.router.projectmanager.project.baseline.node.create import project_baseline_node_create
from gateway.router.projectmanager.project.baseline.node.list import project_baseline_node_list

from gateway.router.filemanager.file.create import file_create
from gateway.router.filemanager.file.list import file_list
from gateway.router.filemanager.file.importfile.upload import file_importfile_upload
from gateway.router.filemanager.file.importfile.upload2 import file_importfile_upload2
from gateway.router.filemanager.file.importfile.uncertaintydetect import file_importfile_uncertaindetect
from gateway.router.filemanager.file.importfile.spreaddetect import file_importfile_spreaddetect
from gateway.router.filemanager.file.delete import file_delete
from gateway.router.filemanager.file.getscope import file_getscope
from gateway.router.filemanager.file.getspread import file_getspread



from gateway.router.requirementmanager.requirement.tree.list import requirement_tree_list
from gateway.router.requirementmanager.requirement.tree.edit import requirement_tree_edit
from gateway.router.requirementmanager.requirement.create import requirement_create
from gateway.router.requirementmanager.requirement.delete import requirement_delete
from gateway.router.requirementmanager.requirement.edit import requirement_edit
from gateway.router.requirementmanager.requirement.profile import requirement_profile
from gateway.router.requirementmanager.requirement.archive.create import requirement_archive_create
from gateway.router.requirementmanager.requirement.archive.profile import requirement_archive_profile
from gateway.router.requirementmanager.requirement.archive.tree.list import requirement_archive_tree_list
from gateway.router.requirementmanager.requirement.importfile.upload import requirement_importfile_upload
from gateway.router.requirementmanager.requirement.importfile.itemize import requirement_importfile_itemize
from gateway.router.requirementmanager.requirement.importfile.create import requirement_importfile_create
from gateway.router.requirementmanager.requirement.analyze.conflict import requirement_analyze_conflict
from gateway.router.requirementmanager.requirement.analyze.relationship import requirement_analyze_relationship
from gateway.router.requirementmanager.requirement.analyze.similarity import requirement_analyze_similarity

from gateway.router.templatemanager.template.create import template_create
from gateway.router.templatemanager.template.edit import template_edit
from gateway.router.templatemanager.template.upload import template_upload
from gateway.router.templatemanager.template.delete import template_delete
from gateway.router.templatemanager.template.list import template_list

from gateway.router.templatemanager.document.list import document_list
from gateway.router.templatemanager.document.create import document_create
from gateway.router.templatemanager.document.delete import document_delete
from gateway.router.templatemanager.document.edit import document_edit
from gateway.router.templatemanager.document.download import document_download
from gateway.router.templatemanager.document.profile import document_profile

from gateway.router.templatemanager.document.comments.classify import comments_classsify
from gateway.router.templatemanager.document.comments.wordcloud import comments_wordcloud
from gateway.router.templatemanager.document.comments.upload import comments_upload
from gateway.router.templatemanager.document.comments.similarity import comments_similarity